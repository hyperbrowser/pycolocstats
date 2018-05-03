from pycolocstats.core.constants import CWL_OUTPUT_FOLDER_NAME


def toHtml(outputFolder=None, stdoutFile=None, stderrFile=None, queryTrack=None, refTrack=None,
           queryTitle=None, refTitle=None):
    from os.path import sep, splitext, exists
    from os import linesep

    rootFolderName = outputFolder.split(sep)[-1] if outputFolder else ""
    queryTrackFn = queryTrack.split(sep)[-1]
    refTrackFn = refTrack.split(sep)[-1]
    htmlFn = "~".join((splitext(queryTrack)[0].split(sep)[-1], splitext(refTrack)[0].split(sep)[-1])) + ".html"

    html = "<!DOCTYPE html>" + linesep
    html += "<html>" + linesep
    html += "<head>" + linesep
    if exists(sep.join((outputFolder, htmlFn))):
        targetHtml = sep.join((CWL_OUTPUT_FOLDER_NAME, rootFolderName, htmlFn))
        contents = ""
        with open(sep.join((outputFolder, htmlFn)), "rt") as f:
            contents = f.read()
        if contents:
            contents = contents.replace(queryTrackFn, queryTitle)
            contents = contents.replace(refTrackFn, refTitle)
            with open(sep.join((outputFolder, htmlFn)), "wt") as f:
                f.write(contents)
        html += "<meta http-equiv=\"refresh\"  content=\"0; url={}\" />".format(targetHtml)
        html += "</head>" + linesep
        html += "<body>" + linesep
        html += "<p><a href=\"{}\">Redirect to full results page</a></p>".format(targetHtml)
    else:
        html += "</head>" + linesep
        html += "<body>" + linesep
        html += "<p>Something went wrong while generating the HTML report.</p>"
        with open(stderrFile, 'rt') as f:
            html += "<p>" + f.read().replace(linesep, "<br>") + "</p>"
    html += "</body>" + linesep
    html += "</html>"
    return html