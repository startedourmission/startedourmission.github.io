module SkunkHtml
    open SkunkUtils
    open System.IO
    open FSharp.Formatting.Markdown
    open System.Text.RegularExpressions

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
            |> (fun md -> Regex.Replace(md, "(?m)^#+\s", "\n<!-- -->\n$0"))

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

                let mainHtmlContent = titleDisplay + Markdown.ToHtml(processedMarkdownContent)
                mainHtmlContent  + giscusScript

        let finalHtmlContent =
            generateFinalHtml (head (" - " + title)) header footer htmlContent highlightingScript

        printfn $"Processing {Path.GetFileName markdownFilePath} ->"
        Disk.writeFile outputHtmlFilePath finalHtmlContent

    let createIndexPage (header: string) (footer: string) (gridSections: (string * Post list) list) (navFolders: string array) (regularPosts: Post list) =
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
                    |> (fun md -> Regex.Replace(md, "(?m)^#+\s", "\n<!-- -->\n$0"))
                Markdown.ToHtml(processedMarkdownContent)
            else
                printfn $"Warning! File {Config.frontPageMarkdownFileName} does not exist! The main page will only contain blog entries, without a welcome message"
                ""

        let gridSectionsHtml =
            gridSections
            |> List.map (fun (title, posts) ->
                let gridContentHtml =
                    posts
                    |> List.map (fun post ->
                        match post.ImageUrl with
                        | Some imageUrl ->
                            $"""
                            <div class="post-card">
                                <a href="{post.Url}">
                                    <img src="{imageUrl}" alt="{post.Title}" class="post-image" />
                                    <h3 class="post-title">{post.Title}</h3>
                                </a>
                            </div>
                            """
                        | None ->
                            $"""
                            <div class="post-card">
                                <a href="{post.Url}">
                                    <div class="post-image-placeholder"></div>
                                    <h3 class="post-title">{post.Title}</h3>
                                </a>
                            </div>
                            """)
                    |> String.concat "\n"
                
                $"""
                <section class="grid-section">
                    <h1 class="grid-title">{title}</h1>
                    <div class="papers-grid">
                    {gridContentHtml}
                    </div>
                </section>
                """)
            |> String.concat "\n"

        // 동적 내비게이션 생성
        let dynamicNavHtml =
            navFolders
            |> Array.map (fun folderName ->
                let urlFriendlyName = Url.toUrlFriendly folderName
                $"""<li><a href="{urlFriendlyName}.html">{folderName}</a></li>""")
            |> String.concat "\n        "

        let updatedHeader = 
            header.Replace("    </ul>", 
                          $"""        {dynamicNavHtml}
    </ul>""")

        // Posts 섹션 (일반 게시물들)
        let postsHtml =
            if regularPosts.IsEmpty then ""
            else
                let postsListHtml =
                    regularPosts
                    |> List.map (fun post -> 
                        let dateHtml = 
                            match post.Date with
                            | Some date -> $"""<span class="post-date">{date.ToString("yyyy-MM-dd")}</span>"""
                            | None -> ""
                        
                        let summaryHtml = 
                            match post.Summary with
                            | Some summary -> $"""<p class="post-summary">{summary}</p>"""
                            | None -> ""
                        
                        $"""
                        <li class="post-item">
                            <div class="post-header">
                                <a href="{post.Url}" class="post-title-link">{post.Title}</a>
                                {dateHtml}
                            </div>
                            {summaryHtml}
                        </li>""")
                    |> String.concat "\n            "
                
                $"""
                <section class="posts-section">
                    <h1 class="posts-title">Posts</h1>
                    <ul class="posts-list">
            {postsListHtml}
                    </ul>
                </section>
                """

        let content =
            $"""
        {frontPageContentHtml}
        {gridSectionsHtml}
        {postsHtml}
        """

        let frontPageHtmlContent = generateFinalHtml (head "") updatedHeader footer content highlightingScript
        let indexHtmlFilePath = Path.Combine(Config.outputDir, "index.html")

        Disk.writeFile indexHtmlFilePath frontPageHtmlContent

    let createCategoryPage (header: string) (footer: string) (categoryName: string) (posts: Post list) (outputPath: string) (navFolders: string array) =
        let postsHtml =
            posts
            |> List.map (fun post -> 
                let dateHtml = 
                    match post.Date with
                    | Some date -> $"""<span class="post-date">{date.ToString("yyyy-MM-dd")}</span>"""
                    | None -> ""
                
                let summaryHtml = 
                    match post.Summary with
                    | Some summary -> $"""<p class="post-summary">{summary}</p>"""
                    | None -> ""
                
                $"""
                <li class="post-item">
                    <div class="post-header">
                        <a href="{post.Url}" class="post-title-link">{post.Title}</a>
                        {dateHtml}
                    </div>
                    {summaryHtml}
                </li>""")
            |> String.concat "\n            "

        // 동적 내비게이션 생성
        let dynamicNavHtml =
            navFolders
            |> Array.map (fun folderName ->
                let urlFriendlyName = Url.toUrlFriendly folderName
                $"""<li><a href="{urlFriendlyName}.html">{folderName}</a></li>""")
            |> String.concat "\n        "

        let updatedHeader = 
            // 이미 동적 내비게이션이 있는지 확인 (첫 번째 폴더 링크로 확인)
            if navFolders.Length > 0 && header.Contains($"<li><a href=\"{Url.toUrlFriendly navFolders.[0]}.html\">") then
                header // 이미 업데이트된 헤더
            else
                header.Replace("    </ul>", 
                              $"""        {dynamicNavHtml}
    </ul>""")

        let content =
            $"""
        <h1>{categoryName}</h1>
        <ul class="category-posts">
            {postsHtml}
        </ul>
        """

        let categoryPageHtml = generateFinalHtml (head $" - {categoryName}") updatedHeader footer content highlightingScript
        
        printfn $"Processing category page: {categoryName} ->"
        Disk.writeFile outputPath categoryPageHtml