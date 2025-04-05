module SkunkHtml
    open SkunkUtils
    open System.IO
    open FSharp.Formatting.Markdown

    let generateFinalHtml (head: string) (header: string) (footer: string) (content: string) (script: string) =
        $"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            {head}
        </head>
        <body>
            <header>
                {header}
            </header>
            <main>
                {content}
            </main>
            <hr />
            <footer>
                {footer}
            </footer>
            <script>
                {script}
            </script>
        </body>
        </html>
        """

    let head (titleSuffix: string) =
        let headTemplate =
            Path.Combine(Config.htmlDir, "head.html")
            |> Disk.readFile

        let titleTemplate =
            Path.Combine(Config.htmlDir, "title.html")
            |> Disk.readFile

        headTemplate.Replace("{{title.html content}}", titleTemplate + titleSuffix)

    let isArticle (file: string) =
        System.Char.IsDigit(Path.GetFileName(file).[0])

    let highlightingScript =
        Path.Combine(Config.htmlDir, "script_syntax_highlighting.html")
        |> Disk.readFile

    let extractTitleFromMarkdownFile (markdownFilePath: string) =
        File.ReadAllLines(markdownFilePath)
        |> Array.tryFind _.StartsWith("# ")
        |> Option.defaultValue "# No Title"
        |> _.TrimStart('#').Trim()

    let createPage (header: string) (footer: string) (markdownFilePath: string) =
        let title = extractTitleFromMarkdownFile(markdownFilePath)
        // 제목에서도 앞부분 숫자 제거 후 URL 친화적으로 변환
        let cleanTitle = Obsidian.removeLeadingNumbers title
        let fileName = Url.toUrlFriendly cleanTitle
        let outputHtmlFilePath = Path.Combine(Config.outputDir, fileName + ".html")
        let markdownContent = File.ReadAllText(markdownFilePath)
        
        // Obsidian 링크 변환 적용
        let processedMarkdownContent = Obsidian.convertWikiLinks markdownContent

        let htmlContent =
            match isArticle markdownFilePath with
            | false -> Markdown.ToHtml(processedMarkdownContent)
            | true ->
                let date = Path.GetFileNameWithoutExtension(markdownFilePath)

                let publicationDate =
                    $"""<p class="publication-date">Published on <time datetime="{date}">{date}</time></p>"""

                let giscusScript =
                    Path.Combine(Config.htmlDir, "script_giscus.html")
                    |> Disk.readFile

                let mainHtmlContent = Markdown.ToHtml(
                    processedMarkdownContent
                    + "\n\n"
                    + publicationDate
                    + "\n\n"
                )
                mainHtmlContent  + giscusScript

        let finalHtmlContent =
            generateFinalHtml (head (" - " + title)) header footer htmlContent highlightingScript

        printfn $"Processing {Path.GetFileName markdownFilePath} ->"
        Disk.writeFile outputHtmlFilePath finalHtmlContent

    let createIndexPage (header: string) (footer: string) (listOfAllBlogArticles: (string * string * string) list) =
        let frontPageMarkdownFilePath = Path.Combine(Config.markdownDir, Config.frontPageMarkdownFileName)

        let frontPageContentHtml =
            if File.Exists(frontPageMarkdownFilePath) then
                printfn $"Processing {Path.GetFileName frontPageMarkdownFilePath} ->"
                // 인덱스 페이지에도 Obsidian 링크 변환 적용
                let markdownContent = File.ReadAllText(frontPageMarkdownFilePath)
                let processedMarkdownContent = Obsidian.convertWikiLinks markdownContent
                Markdown.ToHtml(processedMarkdownContent)
            else
                printfn $"Warning! File {Config.frontPageMarkdownFileName} does not exist! The main page will only contain blog entries, without a welcome message"
                ""

        let listOfAllBlogArticlesContentHtml =
            listOfAllBlogArticles
            |> List.map (fun (date, _, link) -> $"""<li><a href="{link}">{date}</a></li>""")
            |> String.concat "\n"

        let content =
            $"""
        {frontPageContentHtml}
        <section class="publications">
            <h1>Posts</h1>
            <ul>
            {listOfAllBlogArticlesContentHtml}
            </ul>
        </section>
        """

        let frontPageHtmlContent = generateFinalHtml (head "") header footer content highlightingScript
        let indexHtmlFilePath = Path.Combine(Config.outputDir, "index.html")

        Disk.writeFile indexHtmlFilePath frontPageHtmlContent