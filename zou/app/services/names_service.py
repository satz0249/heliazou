import slugify

from zou.app.models.organisation import Organisation
from zou.app.services import (
    entities_service,
    files_service,
    projects_service,
    tasks_service,
    shots_service,
)


def get_full_entity_name(entity_id):
    """
    Get full entity name whether it's an asset or a shot. If it's a shot
    the result is "Episode name / Sequence name / Shot name". If it's an
    asset the result is "Asset type name / Asset name".
    """
    entity = entities_service.get_entity(entity_id)
    episode_id = None
    if shots_service.is_shot(entity):
        sequence = entities_service.get_entity(entity["parent_id"])
        if sequence["parent_id"] is None:
            name = "%s / %s" % (sequence["name"], entity["name"])
        else:
            episode = entities_service.get_entity(sequence["parent_id"])
            episode_id = episode["id"]
            name = "%s / %s / %s" % (
                episode["name"],
                sequence["name"],
                entity["name"],
            )
    else:
        asset_type = entities_service.get_entity_type(entity["entity_type_id"])
        episode_id = entity["source_id"]
        name = "%s / %s" % (asset_type["name"], entity["name"])
    return (name, episode_id)


def get_preview_file_name(preview_file_id):
    """
    Build unique and human readable file name for preview downloads. The
    convention followed is:
    [project_name]_[entity_name]_[task_type_name]_v[revivision].[extension].
    """
    organisation = Organisation.query.first()
    preview_file = files_service.get_preview_file(preview_file_id)
    task = tasks_service.get_task(preview_file["task_id"])
    task_type = tasks_service.get_task_type(task["task_type_id"])
    project = projects_service.get_project(task["project_id"])
    (entity_name, _) = get_full_entity_name(task["entity_id"])

    if (
        organisation.use_original_file_name
        and preview_file.get("original_name", None) is not None
    ):
        name = preview_file["original_name"]
    else:
        name = "%s_%s_%s_v%s" % (
            project["name"],
            entity_name,
            task_type["name"],
            preview_file["revision"],
        )
        name = slugify.slugify(name, separator="_")
    if (preview_file.get("position", 0) or 0) > 1:
        name = "%s-%s" % (name, preview_file["position"])
    return "%s.%s" % (name, preview_file["extension"])
