from osmapi import OsmApi
import pprint
import logging

from config import BaseConfig

from . import errortypes
from . import kort_api

log = logging.getLogger(__name__)


class OsmFix(object):
    def __init__(self):
        osm_user = BaseConfig.OSM_USER
        osm_pass = BaseConfig.OSM_PASSWORD
        osm_api = BaseConfig.OSM_API_URL

        self.osm = OsmApi(
            api=osm_api,
            appid='Kort',
            username=osm_user,
            password=osm_pass
        )
        self.kort_api = kort_api.KortApi()

    def get_for_type(self, type, id):
        """
        Returns the 'getter' of the requested OSM type
        """
        if type == 'node':
            return self.osm.NodeGet(id)
        if type == 'way':
            return self.osm.WayGet(id)
        if type == 'relation':
            return self.osm.RelationGet(id)

    def update_for_type(self, type, new_values):
        """
        Returns the 'update' method of the requested OSM type
        """
        if type == 'node':
            return self.osm.NodeUpdate(new_values)
        if type == 'way':
            return self.osm.WayUpdate(new_values)
        if type == 'relation':
            return self.osm.RelationUpdate(new_values)

    def apply_kort_fix(self, limit=1, dry=False):
        try:
            for kort_fix in self.kort_api.read_fix():
                try:
                    log.debug("---- Fix from Kort: ----")
                    log.debug("%s" % pprint.pformat(kort_fix))


                    osm_entity = self.get_for_type(
                        kort_fix['osm_type'],
                        kort_fix['osm_id']
                    )
                    if not osm_entity:
                        raise OsmEntityNotFoundError("OSM entity not found")

                    log.debug("---- OSM type before fix ----")
                    log.debug("%s" % pprint.pformat(osm_entity['tag']))

                    error_type = errortypes.Error(
                        kort_fix['error_type'],
                        osm_entity
                    )
                    fixed = error_type.apply_fix(kort_fix)
                    fixed_osm_entity, description = fixed

                    log.debug("---- OSM type after fix ----")
                    log.debug("%s" % pprint.pformat(fixed_osm_entity['tag']))
                except (errortypes.ErrorTypeError,
                        OsmEntityNotFoundError,
                        ValueError) as e:
                    log.warning(
                        "The fix could not be applied: %s, fix: %s"
                        % (str(e), kort_fix)
                    )
                    fixed_osm_entity = None
                if not dry:
                    if fixed_osm_entity is not None:
                        comment = self.gen_changelog_comment(
                            kort_fix,
                            description
                        )
                        self.submit_entity(
                            kort_fix['osm_type'],
                            fixed_osm_entity,
                            comment,
                            kort_fix
                        )
                    self.kort_api.mark_fix(kort_fix['fix_id'])
        except Exception as e:
            log.exception("Failed to apply fix of Kort to OpenStreetMap")

    def gen_changelog_comment(self, kort_fix, change_description):
        comment = (
            u"Change from kort, user: %s (id: %s), "
            u"fix id: %s, error: %s (source: %s), "
            u"description: %s, "
            u"see this users profile for more information: "
            u"http://www.openstreetmap.org/user/kort-to-osm"
            % (
                kort_fix['username'],
                kort_fix['user_id'],
                kort_fix['fix_id'],
                kort_fix['error_type'],
                kort_fix['source'],
                change_description
            )
        )
        return comment

    def submit_entity(self, type, entity, comment, kort_fix):
        """
        Submits an OSM entity (node, way, relation) to OSM
        """
        self.osm.ChangesetCreate({
            "comment": comment[:255],
            "mechanical": "yes",
            "kort:username": kort_fix['username'],
            "kort:user_id": str(kort_fix['user_id']),
            "kort:fix_id": str(kort_fix['fix_id']),
            "kort:error_type": kort_fix['error_type'],
            "kort:error_source": kort_fix['source']
        })
        changeset = self.update_for_type(
            type,
            entity
        )
        log.info("%s" % pprint.pformat(changeset))
        self.osm.ChangesetClose()


class OsmEntityNotFoundError(Exception):
    pass
