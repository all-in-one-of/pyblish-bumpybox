import os

import pymel.core as pm
import maya.cmds as mc
import ftrack


def resolutionInit():
    defaultResolution = pm.PyNode("defaultResolution")
    task = ftrack.Task(os.environ["FTRACK_TASKID"])

    # Adding/Checking ftrack resolution attribute
    resolution_set = False
    if hasattr(defaultResolution, "ftrackResolutionSet"):
        attr = pm.Attribute("defaultResolution.ftrackResolutionSet")
        resolution_set = attr.get()
    else:
        pm.addAttr(
            defaultResolution,
            longName="ftrackResolutionSet",
            defaultValue=True,
            attributeType="bool"
        )

    if not resolution_set:
        width = task.getParent().get("width")
        defaultResolution.width.set(width)
        pm.warning("Changed resolution width to: {0}".format(width))
        height = task.getParent().get("height")
        defaultResolution.height.set(height)
        pm.warning("Changed resolution height to: {0}".format(height))


def disableDebug():
    import logging
    logging.getLogger().setLevel(logging.INFO)


def init():
    pm.evalDeferred("ftrack_init.resolutionInit()")

    # Disabling debug logging, cause of FTrack constant stream of print outs.
    mc.evalDeferred('disableDebug()', lowestPriority=True)
