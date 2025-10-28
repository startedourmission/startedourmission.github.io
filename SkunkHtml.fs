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
    
    let headWithMetaTags (titleSuffix: string) (postTitle: string) (description: string option) (imageUrl: string option) (pageUrl: string) =
        let baseHead = head titleSuffix
        let postFullTitle = postTitle + titleSuffix
        
        let ogMetaTags = 
            let titleTag = $"<meta property=\"og:title\" content=\"{postFullTitle}\" />"
            let urlTag = $"<meta property=\"og:url\" content=\"{Config.blogBaseUrl}/{pageUrl}\" />"
            let typeTag = "<meta property=\"og:type\" content=\"article\" />"
            let siteNameTag = $"<meta property=\"og:site_name\" content=\"{Config.blogTitle}\" />"
            
            let descriptionTag = 
                match description with
                | Some desc -> $"<meta property=\"og:description\" content=\"{desc}\" />"
                | None -> ""
            
            let imageTag = 
                match imageUrl with
                | Some img -> $"<meta property=\"og:image\" content=\"{Config.blogBaseUrl}/{img}\" />"
                | None -> ""
            
            $"{titleTag}\n    {urlTag}\n    {typeTag}\n    {siteNameTag}\n    {descriptionTag}\n    {imageTag}"
        
        let twitterMetaTags = 
            let cardTag = "<meta name=\"twitter:card\" content=\"summary_large_image\" />"
            let titleTag = $"<meta name=\"twitter:title\" content=\"{postFullTitle}\" />"
            
            let descriptionTag = 
                match description with
                | Some desc -> $"<meta name=\"twitter:description\" content=\"{desc}\" />"
                | None -> ""
            
            let imageTag = 
                match imageUrl with
                | Some img -> $"<meta name=\"twitter:image\" content=\"{Config.blogBaseUrl}/{img}\" />"
                | None -> ""
            
            $"{cardTag}\n    {titleTag}\n    {descriptionTag}\n    {imageTag}"
        
        baseHead + $"\n    {ogMetaTags}\n    {twitterMetaTags}"
    
    let headCanvas (titleSuffix: string) =
        let headTemplate =
            Path.Combine(Config.htmlDir, "head-canvas.html")
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
    
    let generateTagsHtml (tags: string list) =
        if tags.IsEmpty then
            ""
        else
            let tagLinks = 
                tags
                |> List.map (fun tag -> 
                    let tagUrl = Url.toUrlFriendly tag
                    $"<a href=\"/tag-{tagUrl}.html\" class=\"tag\">{tag}</a>")
                |> String.concat " "
            $"<div class=\"tags\">🏷️ {tagLinks}</div>"

    let createPage (header: string) (footer: string) (markdownFilePath: string) =
        let title = extractTitleFromMarkdownFile(markdownFilePath)
        // 파일명을 URL 친화적으로 변환
        let fileName = Url.toUrlFriendly title
        let outputHtmlFilePath = Path.Combine(Config.outputDir, fileName + ".html")
        let markdownContent = File.ReadAllText(markdownFilePath)
        
        // 메타데이터 추출
        let description = Obsidian.extractDescription markdownContent
        let imageUrl = Obsidian.extractImageUrl markdownContent
        let tags = Obsidian.extractTags markdownContent
        let pageUrl = fileName + ".html"
        
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
                
                // 태그 표시
                let tagsHtml = generateTagsHtml tags

                let giscusScript =
                    Path.Combine(Config.htmlDir, "script_giscus.html")
                    |> Disk.readFile

                let mainHtmlContent = titleDisplay + tagsHtml + Markdown.ToHtml(processedMarkdownContent)
                mainHtmlContent  + giscusScript

        let finalHtmlContent =
            generateFinalHtml (headWithMetaTags (" - " + title) title description imageUrl pageUrl) header footer htmlContent highlightingScript

        printfn $"Processing {Path.GetFileName markdownFilePath} ->"
        Disk.writeFile outputHtmlFilePath finalHtmlContent

    let createIndexPage (header: string) (footer: string) (gridSections: (string * Post list) list) (navFolders: string array) (regularPosts: Post list) (allPosts: Post list) =
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

        // 태그 섹션 생성
        let allTags = 
            allPosts
            |> List.collect (fun post -> post.Tags)
            |> List.distinct
            |> List.sort
        
        let tagsHtml = 
            if allTags.IsEmpty then 
                ""
            else
                let tagLinks = 
                    allTags
                    |> List.map (fun tag -> 
                        let tagUrl = Url.toUrlFriendly tag
                        $"<a href=\"/tag-{tagUrl}.html\">{tag}</a>")
                    |> String.concat " · "
                $"""
                <section class="tags-section">
                    <h2>Tags</h2>
                    <p>{tagLinks}</p>
                </section>
                """

        // 동적 내비게이션 생성 (Posts + 그리드 섹션들 + navFolders)
        let gridNavHtml =
            gridSections
            |> List.map (fun (title, _) ->
                let urlFriendlyName = Url.toUrlFriendly title
                $"""<li><a href="{urlFriendlyName}.html">{title}</a></li>""")
            |> String.concat "\n        "

        let navFoldersHtml =
            navFolders
            |> Array.map (fun folderName ->
                let urlFriendlyName = Url.toUrlFriendly folderName
                $"""<li><a href="{urlFriendlyName}.html">{folderName}</a></li>""")
            |> String.concat "\n        "

        let dynamicNavHtml =
            $"""<li><a href="posts.html">Posts</a></li>
        {gridNavHtml}
        {navFoldersHtml}"""

        let updatedHeader =
            header.Replace("    </ul>",
                          $"""        {dynamicNavHtml}
    </ul>""")

        // Headliner 섹션 (Headliner 태그를 가진 글들)
        let headlinerPosts =
            allPosts
            |> List.filter (fun post -> post.Tags |> List.exists (fun tag -> tag.ToLower() = "headliner"))

        let headlinerHtml =
            if headlinerPosts.IsEmpty then ""
            else
                let headlinerListHtml =
                    headlinerPosts
                    |> List.map (fun post ->
                        let dateHtml =
                            match post.Date with
                            | Some date -> $"""<span class="post-date">{date.ToString("yyyy-MM-dd")}</span>"""
                            | None -> ""

                        let descriptionHtml =
                            match post.Description with
                            | Some description -> $"""<p class="post-summary">{description}</p>"""
                            | None -> ""

                        let imageHtml =
                            match post.ImageUrl with
                            | Some imageUrl -> $"""<img src="{imageUrl}" alt="{post.Title}" class="post-thumbnail" />"""
                            | None -> """<div class="post-thumbnail-empty"></div>"""

                        $"""
                        <li class="post-item">
                            {imageHtml}
                            <div class="post-content">
                                <div class="post-header">
                                    <a href="{post.Url}" class="post-title-link">{post.Title}</a>
                                    {dateHtml}
                                </div>
                                {descriptionHtml}
                            </div>
                        </li>""")
                    |> String.concat "\n            "

                $"""
                <section class="posts-section">
                    <h2 class="posts-title">Headline</h2>
                    <ul class="posts-list posts-with-images">
            {headlinerListHtml}
                    </ul>
                </section>
                """

        let content =
            $"""
        {frontPageContentHtml}
        {headlinerHtml}
        {tagsHtml}
        """

        let frontPageHtmlContent = generateFinalHtml (head "") updatedHeader footer content highlightingScript
        let indexHtmlFilePath = Path.Combine(Config.outputDir, "index.html")

        Disk.writeFile indexHtmlFilePath frontPageHtmlContent

    let createCategoryPage (header: string) (footer: string) (categoryName: string) (posts: Post list) (outputPath: string) (navFolders: string array) (gridFolders: (string * Post list) list) =
        let postsHtml =
            posts
            |> List.map (fun post ->
                let dateHtml =
                    match post.Date with
                    | Some date -> $"""<span class="post-date">{date.ToString("yyyy-MM-dd")}</span>"""
                    | None -> ""

                let descriptionHtml =
                    match post.Description with
                    | Some description -> $"""<p class="post-summary">{description}</p>"""
                    | None -> ""

                let imageHtml =
                    match post.ImageUrl with
                    | Some imageUrl -> $"""<img src="{imageUrl}" alt="{post.Title}" class="post-thumbnail" />"""
                    | None -> """<div class="post-thumbnail-empty"></div>"""

                $"""
                <li class="post-item">
                    {imageHtml}
                    <div class="post-content">
                        <div class="post-header">
                            <a href="{post.Url}" class="post-title-link">{post.Title}</a>
                            {dateHtml}
                        </div>
                        {descriptionHtml}
                    </div>
                </li>""")
            |> String.concat "\n            "

        // 동적 내비게이션 생성 (Posts + 그리드 섹션들 + navFolders)
        let gridNavHtml =
            gridFolders
            |> List.map (fun (title, _) ->
                let urlFriendlyName = Url.toUrlFriendly title
                $"""<li><a href="{urlFriendlyName}.html">{title}</a></li>""")
            |> String.concat "\n        "

        let navFoldersHtml =
            navFolders
            |> Array.map (fun folderName ->
                let urlFriendlyName = Url.toUrlFriendly folderName
                $"""<li><a href="{urlFriendlyName}.html">{folderName}</a></li>""")
            |> String.concat "\n        "

        let dynamicNavHtml =
            $"""<li><a href="posts.html">Posts</a></li>
        {gridNavHtml}
        {navFoldersHtml}"""

        let updatedHeader =
            header.Replace("    </ul>",
                          $"""        {dynamicNavHtml}
    </ul>""")

        let content =
            $"""
        <h1>{categoryName}</h1>
        <ul class="posts-list posts-with-images">
            {postsHtml}
        </ul>
        """

        let categoryPageHtml = generateFinalHtml (head $" - {categoryName}") updatedHeader footer content highlightingScript

        printfn $"Processing category page: {categoryName} ->"
        Disk.writeFile outputPath categoryPageHtml

    let createPostsPage (header: string) (footer: string) (posts: Post list) (outputPath: string) (navFolders: string array) (gridFolders: (string * Post list) list) =
        let postsHtml =
            posts
            |> List.map (fun post ->
                let dateHtml =
                    match post.Date with
                    | Some date -> $"""<span class="post-date">{date.ToString("yyyy-MM-dd")}</span>"""
                    | None -> ""

                let descriptionHtml =
                    match post.Description with
                    | Some description -> $"""<p class="post-summary">{description}</p>"""
                    | None -> ""

                let imageHtml =
                    match post.ImageUrl with
                    | Some imageUrl -> $"""<img src="{imageUrl}" alt="{post.Title}" class="post-thumbnail" />"""
                    | None -> """<div class="post-thumbnail-empty"></div>"""

                $"""
                <li class="post-item">
                    {imageHtml}
                    <div class="post-content">
                        <div class="post-header">
                            <a href="{post.Url}" class="post-title-link">{post.Title}</a>
                            {dateHtml}
                        </div>
                        {descriptionHtml}
                    </div>
                </li>""")
            |> String.concat "\n            "

        // 동적 내비게이션 생성 (Posts + 그리드 섹션들 + navFolders)
        let gridNavHtml =
            gridFolders
            |> List.map (fun (title, _) ->
                let urlFriendlyName = Url.toUrlFriendly title
                $"""<li><a href="{urlFriendlyName}.html">{title}</a></li>""")
            |> String.concat "\n        "

        let navFoldersHtml =
            navFolders
            |> Array.map (fun folderName ->
                let urlFriendlyName = Url.toUrlFriendly folderName
                $"""<li><a href="{urlFriendlyName}.html">{folderName}</a></li>""")
            |> String.concat "\n        "

        let dynamicNavHtml =
            $"""<li><a href="posts.html">Posts</a></li>
        {gridNavHtml}
        {navFoldersHtml}"""

        let updatedHeader =
            header.Replace("    </ul>",
                          $"""        {dynamicNavHtml}
    </ul>""")

        let content =
            $"""
        <h1>Posts</h1>
        <ul class="posts-list posts-with-images">
            {postsHtml}
        </ul>
        """

        let postsPageHtml = generateFinalHtml (head " - Posts") updatedHeader footer content highlightingScript

        printfn $"Processing Posts page ->"
        Disk.writeFile outputPath postsPageHtml

    let createGridSectionPage (header: string) (footer: string) (sectionTitle: string) (posts: Post list) (outputPath: string) (navFolders: string array) (gridFolders: (string * Post list) list) =
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

        // 동적 내비게이션 생성 (Posts + 그리드 섹션들 + navFolders)
        let gridNavHtml =
            gridFolders
            |> List.map (fun (title, _) ->
                let urlFriendlyName = Url.toUrlFriendly title
                $"""<li><a href="{urlFriendlyName}.html">{title}</a></li>""")
            |> String.concat "\n        "

        let navFoldersHtml =
            navFolders
            |> Array.map (fun folderName ->
                let urlFriendlyName = Url.toUrlFriendly folderName
                $"""<li><a href="{urlFriendlyName}.html">{folderName}</a></li>""")
            |> String.concat "\n        "

        let dynamicNavHtml =
            $"""<li><a href="posts.html">Posts</a></li>
        {gridNavHtml}
        {navFoldersHtml}"""

        let updatedHeader =
            header.Replace("    </ul>",
                          $"""        {dynamicNavHtml}
    </ul>""")

        let content =
            $"""
        <section class="grid-section">
            <h1 class="grid-title">{sectionTitle}</h1>
            <div class="papers-grid">
            {gridContentHtml}
            </div>
        </section>
        """

        let gridPageHtml = generateFinalHtml (head $" - {sectionTitle}") updatedHeader footer content highlightingScript

        printfn $"Processing {sectionTitle} page ->"
        Disk.writeFile outputPath gridPageHtml

    let createCanvasPage (header: string) (footer: string) (canvas: Canvas) (outputPath: string) (navFolders: string array) =
        // Canvas 데이터를 JSON으로 직렬화
        let nodesJson =
            canvas.Nodes
            |> List.map (fun node ->
                let textField = 
                    match node.Text with
                    | Some text -> 
                        let escapedText = text.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n").Replace("\r", "\\r").Replace("\t", "\\t")
                        $""", "text": "{escapedText}" """
                    | None -> ""
                let fileField = 
                    match node.File with
                    | Some file -> $""", "file": "{file}" """
                    | None -> ""
                $"""{{"id": "{node.Id}", "type": "{node.Type}"{textField}{fileField}, "x": {node.X}, "y": {node.Y}, "width": {node.Width}, "height": {node.Height}}}""")
            |> String.concat ", "

        let edgesJson =
            canvas.Edges
            |> List.map (fun edge ->
                let fromSideField = 
                    match edge.FromSide with
                    | Some side -> $""", "fromSide": "{side}" """
                    | None -> ""
                let toSideField = 
                    match edge.ToSide with
                    | Some side -> $""", "toSide": "{side}" """
                    | None -> ""
                $"""{{"id": "{edge.Id}", "fromNode": "{edge.FromNode}", "toNode": "{edge.ToNode}"{fromSideField}{toSideField}}}""")
            |> String.concat ", "

        let canvasJson = $"""{{ "nodes": [{nodesJson}], "edges": [{edgesJson}] }}"""

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

        let content =
            $"""
        <h1 class="canvas-title">{canvas.Title}</h1>
        <div id="canvas-container">
            <div id="canvas-visualization"></div>
            <div id="canvas-controls">
                <button id="reset-zoom" class="canvas-btn">Reset Zoom</button>
                <button id="center-view" class="canvas-btn">Center View</button>
            </div>
        </div>
        <div id="node-details" class="node-details-panel" style="display: none;">
            <h3 id="node-title">Node Details</h3>
            <div id="node-content" class="node-content"></div>
            <button id="close-details" class="canvas-btn">Close</button>
        </div>
        
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
            window.canvasData = {canvasJson};
        </script>
        <script src="scripts/canvas-visualization.js"></script>
        """

        let canvasPageHtml = generateFinalHtml (headCanvas $" - {canvas.Title}") updatedHeader footer content ""
        
        printfn $"Processing canvas page: {canvas.Title} ->"
        Disk.writeFile outputPath canvasPageHtml
    
    let createTagPage (header: string) (footer: string) (tagName: string) (tagPosts: Post list) (outputPath: string) (navFolders: string array) =
        let postListHtml =
            tagPosts
            |> List.map (fun post ->
                let dateStr = 
                    match post.Date with
                    | Some date -> date.ToString("yyyy-MM-dd")
                    | None -> ""
                
                let summaryStr = 
                    match post.Summary with
                    | Some summary -> $"<p class=\"post-summary\">{summary}</p>"
                    | None -> ""
                
                $"""
                <article class="post-preview">
                    <h3><a href="{post.Url}">{post.Title}</a></h3>
                    <div class="post-meta">
                        <time datetime="{dateStr}">{dateStr}</time>
                        {if post.Tags.Length > 0 then generateTagsHtml post.Tags else ""}
                    </div>
                    {summaryStr}
                </article>
                """)
            |> String.concat "\n"
        
        let content = 
            $"""
            <h1>태그: {tagName}</h1>
            <p>{tagPosts.Length}개의 게시물</p>
            <div class="posts-list">
                {postListHtml}
            </div>
            """
        
        let dynamicNavHtml = 
            navFolders
            |> Array.map (fun folderName -> 
                let urlFriendlyName = Url.toUrlFriendly folderName
                $"<li><a href=\"{urlFriendlyName}.html\">{folderName}</a></li>")
            |> String.concat "\n        "
        let updatedHeader = 
            header.Replace("    </ul>", 
                          $"""        {dynamicNavHtml}
    </ul>""")
        let tagPageHtml = generateFinalHtml (head $" - 태그: {tagName}") updatedHeader footer content ""
        
        printfn $"Processing tag page: {tagName} -> {tagPosts.Length} posts"
        Disk.writeFile outputPath tagPageHtml

    let createRssFeed (posts: Post list) =
        let items =
            posts
            |> List.map (fun post ->
                let postUrl = $"{Config.blogBaseUrl}/{System.Uri.EscapeUriString(post.Url)}"
                let pubDate =
                    match post.Date with
                    // RFC 822 format
                    | Some date -> date.ToUniversalTime().ToString("R")
                    | None -> ""

                // description은 YAML의 description 사용
                let description =
                    match post.Description with
                    | Some desc -> $"<![CDATA[\n  {desc}\n]]>"
                    | None -> "<![CDATA[]]>"

                // enclosure 태그 생성 (이미지가 있는 경우)
                let enclosureTag =
                    match post.ImageUrl with
                    | Some imageUrl ->
                        let absoluteImageUrl = $"{Config.blogBaseUrl}/{System.Uri.EscapeUriString(imageUrl)}"
                        let imageType = 
                            let ext = Path.GetExtension(imageUrl)
                            if ext.Length > 1 then $"image/{ext.Substring(1).ToLower()}" else "image/png"
                        // length는 0으로 설정 (실제 파일 크기를 알 수 없으므로)
                        $"\n<enclosure url=\"{absoluteImageUrl}\" type=\"{imageType}\" length=\"0\"/>"
                    | None -> ""

                $"""<item>
<title><![CDATA[ {post.Title} ]]></title>
<link>{postUrl}</link>
<guid isPermaLink="true">{postUrl}</guid>
<pubDate>{pubDate}</pubDate>

<description>{description}</description>{enclosureTag}
</item>"""
            )
            |> String.concat "\n"

        let latestBuildDate =
            posts
            |> List.choose (fun p -> p.Date)
            |> List.sortByDescending id
            |> List.tryHead
            |> Option.map (fun dt -> dt.ToUniversalTime().ToString("R"))
            |> Option.defaultValue (System.DateTime.UtcNow.ToString("R"))

        let rssXml =
            $"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>{Config.blogTitle}</title>
    <link>{Config.blogBaseUrl}</link>
    <description>{Config.blogDescription}</description>
    <language>ko-kr</language>
    <lastBuildDate>{latestBuildDate}</lastBuildDate>
    <atom:link href="{Config.blogBaseUrl}/rss.xml" rel="self" type="application/rss+xml" />
    {items}
</channel>
</rss>"""
        let rssFilePath = Path.Combine(Config.outputDir, "rss.xml")
        Disk.writeFile rssFilePath rssXml