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

    // 모든 마크다운 파일을 블로그 글로 처리
    let isArticle (file: string) =
        true  // 모든 .md 파일이 블로그 글로 처리됨

    let highlightingScript =
        Path.Combine(Config.htmlDir, "script_syntax_highlighting.html")
        |> Disk.readFile

    // 파일명에서 제목 추출 (확장자 제외)
    let extractTitleFromMarkdownFile (markdownFilePath: string) =
        Path.GetFileNameWithoutExtension(markdownFilePath)

    let createPage (header: string) (footer: string) (markdownFilePath: string) =
        let title = extractTitleFromMarkdownFile(markdownFilePath)
        // 파일명을 URL 친화적으로 변환
        let fileName = Url.toUrlFriendly title
        let outputHtmlFilePath = Path.Combine(Config.outputDir, fileName + ".html")
        let markdownContent = File.ReadAllText(markdownFilePath)
        
        // 마크다운 전처리: YAML 프론트매터 제거 후 Obsidian 링크 변환
        let processedMarkdownContent = 
            markdownContent
            |> Obsidian.removeYamlFrontMatter
            |> Obsidian.convertWikiLinks

        let htmlContent =
            match isArticle markdownFilePath with
            | false -> Markdown.ToHtml(processedMarkdownContent)
            | true ->
                let date = Path.GetFileNameWithoutExtension(markdownFilePath)
                
                // 파일명을 게시글 상단에 표시
                let titleDisplay = $"<h1 class=\"post-title\">{date}</h1>"

                let giscusScript =
                    Path.Combine(Config.htmlDir, "script_giscus.html")
                    |> Disk.readFile

                let mainHtmlContent = titleDisplay + Markdown.ToHtml(
                    processedMarkdownContent
                    + "\n\n"
                    + "\n\n"
                )
                mainHtmlContent  + giscusScript

        let finalHtmlContent =
            generateFinalHtml (head (" - " + title)) header footer htmlContent highlightingScript

        printfn $"Processing {Path.GetFileName markdownFilePath} ->"
        Disk.writeFile outputHtmlFilePath finalHtmlContent

    let createIndexPage (header: string) (footer: string) (listOfAllBlogArticles: (string * string * string) list) (paperArticles: (string * string * string) list) =
        let frontPageMarkdownFilePath = Path.Combine(Config.markdownDir, Config.frontPageMarkdownFileName)

        let frontPageContentHtml =
            if File.Exists(frontPageMarkdownFilePath) then
                printfn $"Processing {Path.GetFileName frontPageMarkdownFilePath} ->"
                // 인덱스 페이지도 YAML 프론트매터 제거 및 Obsidian 링크 변환 적용
                let markdownContent = File.ReadAllText(frontPageMarkdownFilePath)
                let processedMarkdownContent = 
                    markdownContent
                    |> Obsidian.removeYamlFrontMatter
                    |> Obsidian.convertWikiLinks
                Markdown.ToHtml(processedMarkdownContent)
            else
                printfn $"Warning! File {Config.frontPageMarkdownFileName} does not exist! The main page will only contain blog entries, without a welcome message"
                ""

        let listOfAllBlogArticlesContentHtml =
            listOfAllBlogArticles
            |> List.map (fun (date, _, link) -> $"""<li><a href="{link}">{date}</a></li>""")
            |> String.concat "\n"

        let paperArticlesContentHtml =
            paperArticles
            |> List.map (fun (date, _, link) -> $"""<li><a href="{link}">{date}</a></li>""")
            |> String.concat "\n"

        let content =
            $"""
        {frontPageContentHtml}
        <div class="publications-container">
            <section class="publications papers">
                <h1>Papers</h1>
                <ul>
                {paperArticlesContentHtml}
                </ul>
            </section>
            <section class="publications posts">
                <h1>Posts</h1>
                <ul>
                {listOfAllBlogArticlesContentHtml}
                </ul>
            </section>
        </div>
        """

        let frontPageHtmlContent = generateFinalHtml (head "") header footer content highlightingScript
        let indexHtmlFilePath = Path.Combine(Config.outputDir, "index.html")

        Disk.writeFile indexHtmlFilePath frontPageHtmlContent