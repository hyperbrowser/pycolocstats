def toHtml(outputFolder=None, stdoutFile=None, stderrFile=None, urlPrefix=''):

    from os import linesep, path
    from pycolocstats.core.constants import CWL_OUTPUT_FOLDER_NAME

    htmlStr = '''
    <html>
        <head>
            <style>
            table, th, td {
                border: 1px solid grey;
            }
            </style>
            <script type="text/javascript" src="''' + urlPrefix + '''/static/scripts/libs/jquery/jquery.js"></script>
            <script type="text/javascript" src="''' + urlPrefix + '''/static/scripts/proto/sorttable.js"></script>
        </head>
        <body>
            <h3> Intervalstats results: </h3>
            <table border="1|0" class="sortable" width="100%%" style="table-layout:auto;word-wrap:break-word;">
                <tr>
                    <th bgcolor="lightgray">Query interval</th>
                    <th bgcolor="lightgray">Closest reference interval</th>
                    <th bgcolor="lightgray">Length of query</th>
                    <th bgcolor="lightgray">Distance</th>
                    <th bgcolor="lightgray">Numerator</th>
                    <th bgcolor="lightgray">Denominator</th>
                    <th bgcolor="lightgray">P-value</th>
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
