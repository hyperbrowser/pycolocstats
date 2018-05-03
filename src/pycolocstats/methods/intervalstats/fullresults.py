def toHtml(outputFolder=None, stdoutFile=None, stderrFile=None, urlPrefix=''):

    from os import linesep, path
    from pycolocstats.core.constants import CWL_OUTPUT_FOLDER_NAME

    htmlStr = '''
    <html>
        <head>
            <script type="text/javascript" src="''' + urlPrefix + '''/static/scripts/libs/jquery/jquery.js"></script>
            <script type="text/javascript" src="''' + urlPrefix + '''/static/scripts/proto/sorttable.js"></script>
        </head>
        <body>
            <h3> Intervalstats results: </h3>
            <table class="sortable" width="100%%" style="table-layout:auto;word-wrap:break-word;border: 1px solid grey;">
                <tr>
                    <th>Query interval</th>
                    <th>Closest reference interval</th>
                    <th>Length of query</th>
                    <th>Distance</th>
                    <th>Numerator</th>
                    <th>Denominator</th>
                    <th>P-value</th>
                </tr>
    '''
    with open(path.join(outputFolder, 'output'), 'rt') as f:
        for line in f.readlines():
            htmlStr += "                <tr>" + linesep
            for cell in line.split():
                htmlStr += "                    <td>" + cell + "</td>" + linesep
            htmlStr += "                </tr>" + linesep

    htmlStr += '''
            </table>
            <p>
            '''
    rootFolderName = outputFolder.split(path.sep)[-1] if outputFolder else ""
    htmlStr += "<a href = \"" + CWL_OUTPUT_FOLDER_NAME + path.sep + rootFolderName + path.sep + "output\"> Raw output </a>" + linesep

    htmlStr += '''
            </p>
        </body>
    </html>
    '''

    return htmlStr
