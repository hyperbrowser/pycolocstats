from pycolocstats.core.constants import CWL_OUTPUT_FOLDER_NAME


def toHtml(outputFolder=None, stdoutFile=None, stderrFile=None, queryTrack=None, refTrack=None):
    from os.path import sep, splitext
    from os import linesep
    rootFolderName = outputFolder.split(sep)[-1] if outputFolder else ""
    htmlFn = "~".join((splitext(queryTrack)[0].split(sep)[-1], splitext(refTrack)[0].split(sep)[-1])) + ".html"
    targetHtml = sep.join((CWL_OUTPUT_FOLDER_NAME, rootFolderName, htmlFn))

    html = "<!DOCTYPE html>" + linesep
    html += "<html>" + linesep
    html += "<head>" + linesep
    html += "<meta http-equiv=\"refresh\"  content=\"0; url={}\" />".format(targetHtml)
    html += "</head>" + linesep
    html += "<body>" + linesep
    html += "<p><a href=\"{}\">Redirect to full results page</a></p>".format(targetHtml)
    html += "</body>" + linesep
    html += "</html>"
    return html