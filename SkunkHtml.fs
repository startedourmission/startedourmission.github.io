module SkunkHtml
    open SkunkUtils
    open System.IO
    open System.Net
    open FSharp.Formatting.Markdown
    open System.Text.RegularExpressions

    let escHtml (s: string) = WebUtility.HtmlEncode(s)
    let escJson (s: string) = s.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n").Replace("\r", "")

    /// %%arch:preset_name%% 텍스트 마커를 인터랙티브 플로차트 div로 변환
    let expandArchMarkers (html: string) =
        Regex.Replace(html, @"<p>\s*%%arch:(\w+)%%\s*</p>", """<div class="arch-flow" data-arch="$1"></div>""")

    let generateFinalHtml (head: string) (header: string) (footer: string) (content: string) (script: string) =
        $"""
        <!DOCTYPE html>
        <html lang="ko-KR">
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
    
    let headWithCanonical (titleSuffix: string) (pageUrl: string) =
        let baseHead = head titleSuffix
        let canonicalTag = $"<link rel=\"canonical\" href=\"{Config.blogBaseUrl}/{pageUrl}\" />"
        baseHead + $"\n    {canonicalTag}"

    let headWithMetaTags (titleSuffix: string) (postTitle: string) (description: string option) (imageUrl: string option) (pageUrl: string) (date: System.DateTime option) (tags: string list) =
        let baseHead = head titleSuffix
        let postFullTitle = postTitle + titleSuffix
        let fullUrl = $"{Config.blogBaseUrl}/{pageUrl}"

        // description이 있으면 기본 meta description 교체 (HTML 이스케이핑 적용)
        let headWithDesc =
            match description with
            | Some desc ->
                baseHead.Replace(
                    "<meta name=\"description\" content=\"Papers, Books, and Projects that started our mission.\" />",
                    $"<meta name=\"description\" content=\"{escHtml desc}\" />")
            | None -> baseHead

        let canonicalTag = $"<link rel=\"canonical\" href=\"{fullUrl}\" />"

        let ogMetaTags =
            let titleTag = $"<meta property=\"og:title\" content=\"{escHtml postTitle}\" />"
            let urlTag = $"<meta property=\"og:url\" content=\"{fullUrl}\" />"
            let typeTag = "<meta property=\"og:type\" content=\"article\" />"
            let siteNameTag = $"<meta property=\"og:site_name\" content=\"{escHtml Config.blogTitle}\" />"

            let descriptionTag =
                match description with
                | Some desc -> $"<meta property=\"og:description\" content=\"{escHtml desc}\" />"
                | None -> ""

            let defaultImage = $"{Config.blogBaseUrl}/assets/notion_avatar.png"
            let imageTag =
                match imageUrl with
                | Some img -> $"<meta property=\"og:image\" content=\"{Config.blogBaseUrl}/{img}\" />"
                | None -> $"<meta property=\"og:image\" content=\"{defaultImage}\" />"

            $"{titleTag}\n    {urlTag}\n    {typeTag}\n    {siteNameTag}\n    {descriptionTag}\n    {imageTag}"

        let twitterMetaTags =
            let defaultImage = $"{Config.blogBaseUrl}/assets/notion_avatar.png"
            let cardTag = "<meta name=\"twitter:card\" content=\"summary_large_image\" />"
            let titleTag = $"<meta name=\"twitter:title\" content=\"{escHtml postTitle}\" />"

            let descriptionTag =
                match description with
                | Some desc -> $"<meta name=\"twitter:description\" content=\"{escHtml desc}\" />"
                | None -> ""

            let imageTag =
                match imageUrl with
                | Some img -> $"<meta name=\"twitter:image\" content=\"{Config.blogBaseUrl}/{img}\" />"
                | None -> $"<meta name=\"twitter:image\" content=\"{defaultImage}\" />"

            $"{cardTag}\n    {titleTag}\n    {descriptionTag}\n    {imageTag}"

        // JSON-LD BlogPosting 구조화 데이터 (JSON 이스케이핑 적용)
        let jsonLd =
            let datePublished =
                match date with
                | Some d -> $""","datePublished":"{d.ToString("yyyy-MM-dd")}" """
                | None -> ""
            let keywordsField =
                if tags.IsEmpty then ""
                else
                    let joined = tags |> List.map (fun t -> $"\"{escJson t}\"") |> String.concat ","
                    $""","keywords":[{joined}]"""
            let descField =
                match description with
                | Some desc -> $""","description":"{escJson desc}" """
                | None -> ""
            let imageField =
                match imageUrl with
                | Some img -> $""","image":"{Config.blogBaseUrl}/{img}" """
                | None -> $""","image":"{Config.blogBaseUrl}/assets/notion_avatar.png" """
            $"""<script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"BlogPosting","headline":"{escJson postTitle}","url":"{fullUrl}","author":{{"@type":"Person","name":"Cha Jinwoo"}}{datePublished}{descField}{imageField}{keywordsField}}}
    </script>"""

        headWithDesc + $"\n    {canonicalTag}\n    {ogMetaTags}\n    {twitterMetaTags}\n    {jsonLd}"
    
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
    
    let buildNav (header: string) (gridSections: (string * Post list) list) (navFolders: string array) =
        let gridNavItems =
            gridSections
            |> List.map (fun (title, _) ->
                let urlFriendlyName = Url.toUrlFriendly title
                $"""<li><a href="{urlFriendlyName}.html">{title}</a></li>""")

        let navFolderItems =
            navFolders
            |> Array.toList
            |> List.map (fun folderName ->
                let urlFriendlyName = Url.toUrlFriendly folderName
                $"""<li><a href="{urlFriendlyName}.html">{folderName}</a></li>""")

        let mainItems = gridNavItems
        let subItems = navFolderItems

        let mainHtml = mainItems |> String.concat "\n        "
        let subHtml = subItems |> String.concat "\n        "

        let navBlock =
            $"""<ul class="nav-main">
        {mainHtml}
    </ul>"""
            + (if subItems.Length > 0 then
                   $"""
    <ul class="nav-sub">
        {subHtml}
    </ul>"""
               else "")

        header.Replace("""<ul>
    </ul>""", navBlock)

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
        // 파일명 해시 기반 URL (한글 제목도 짧고 깔끔한 URL)
        let fileName = Url.toHashId title
        let outputHtmlFilePath = Path.Combine(Config.outputDir, fileName + ".html")
        let markdownContent = File.ReadAllText(markdownFilePath)
        
        // 메타데이터 추출
        let description = Obsidian.extractDescription markdownContent
        let imageUrl = Obsidian.extractImageUrl markdownFilePath markdownContent
        let tags = Obsidian.extractTags markdownContent
        let date = Obsidian.extractDate markdownContent title
        let pageUrl = fileName + ".html"

        // 마크다운 전처리: YAML 프론트매터 제거 후 Obsidian 링크 변환
        let processedMarkdownContent =
            markdownContent
            |> Obsidian.removeYamlFrontMatter
            |> Obsidian.convertWikiLinks markdownFilePath
            |> (fun md -> Regex.Replace(md, "(?m)^#+\s", "\n<!-- -->\n$0"))

        let htmlContent =
            match isArticle markdownFilePath with
            | false -> Markdown.ToHtml(processedMarkdownContent) |> expandArchMarkers
            | true ->
                let date = Path.GetFileNameWithoutExtension(markdownFilePath)

                // 파일명을 게시글 상단에 표시
                let titleDisplay = $"<h1 class=\"post-title\">{date}</h1>"

                // 태그 표시
                let tagsHtml = generateTagsHtml tags

                let giscusScript =
                    Path.Combine(Config.htmlDir, "script_giscus.html")
                    |> Disk.readFile

                let mainHtmlContent = titleDisplay + tagsHtml + (Markdown.ToHtml(processedMarkdownContent) |> expandArchMarkers)
                mainHtmlContent  + giscusScript

        let finalHtmlContent =
            generateFinalHtml (headWithMetaTags (" - " + title) title description imageUrl pageUrl date tags) header footer htmlContent highlightingScript

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
                    |> Obsidian.convertWikiLinks frontPageMarkdownFilePath
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
                        $"<a href=\"/tag-{tagUrl}.html\" class=\"tag-filter\" data-tag=\"{escHtml tag}\">{tag}</a>")
                    |> String.concat " · "
                $"""
                <section class="tags-section">
                    <h2>Tags</h2>
                    <p>{tagLinks}</p>
                </section>
                """

        let updatedHeader = buildNav header gridSections navFolders

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
                            | None -> """<img src="assets/notion_avatar.png" alt="Default" class="post-thumbnail" />"""

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

        // Stars 섹션 (Star 태그를 가진 person 노트, buzz/star 점수 내림차순 top 20)
        let starPosts =
            allPosts
            |> List.filter (fun post -> post.Tags |> List.exists (fun tag -> tag.ToLower() = "star"))
            |> List.sortByDescending (fun post -> post.Buzz |> Option.defaultValue 0)
            |> List.truncate 20

        let starsHtml =
            if starPosts.IsEmpty then ""
            else
                let starItemsHtml =
                    starPosts
                    |> List.map (fun post ->
                        let avatarHtml =
                            match post.ImageUrl with
                            | Some imageUrl -> $"""<img src="{imageUrl}" alt="{post.Title}" class="star-avatar" />"""
                            | None -> """<img src="assets/notion_avatar.png" alt="avatar" class="star-avatar" />"""
                        $"""
                        <li class="star-item">
                            <a href="{post.Url}" class="star-link">
                                {avatarHtml}
                                <span class="star-name">{post.Title}</span>
                            </a>
                        </li>""")
                    |> String.concat "\n            "
                $"""
                <section class="stars-section">
                    <h2 class="stars-title">Masters</h2>
                    <ul class="stars-list">
            {starItemsHtml}
                    </ul>
                </section>
                """

        // 검색 인덱스 직렬화 (제목 · 설명 · 태그 · 카테고리 · 날짜로 클라이언트 검색)
        let searchIndexJson =
            allPosts
            |> List.map (fun post ->
                let descStr =
                    match post.Description with
                    | Some d -> d
                    | None -> ""
                let dateStr =
                    match post.Date with
                    | Some d -> d.ToString("yyyy-MM-dd")
                    | None -> ""
                let tagsJson =
                    post.Tags
                    |> List.map (fun t -> $"\"{escJson t}\"")
                    |> String.concat ","
                $"""{{"title":"{escJson post.Title}","url":"{escJson post.Url}","description":"{escJson descStr}","category":"{escJson post.Category}","date":"{escJson dateStr}","tags":[{tagsJson}]}}""")
            |> String.concat ","
        let searchDataJson = $"""[{searchIndexJson}]"""
        let searchViewHtml = $"""
                <section class="search-section">
                    <div class="search-box">
                        <input type="search" id="search-input" class="search-input" placeholder="제목 · 내용 · 태그 검색" autocomplete="off" aria-label="글 검색" />
                        <button id="search-clear" class="search-clear" type="button" aria-label="검색 초기화">&times;</button>
                    </div>
                    <div id="search-active-tags" class="search-active-tags"></div>
                    <div id="search-results" class="search-results" hidden></div>
                </section>
                <script>window.searchData = {searchDataJson};</script>
                <script src="scripts/search.js"></script>
                """

        let content =
            $"""
        {frontPageContentHtml}
        {searchViewHtml}
        {starsHtml}
        {headlinerHtml}
        {tagsHtml}
        """

        let indexOgTags =
            $"""<meta property="og:title" content="{escHtml Config.blogTitle}" />
    <meta property="og:url" content="{Config.blogBaseUrl}/" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="{escHtml Config.blogTitle}" />
    <meta property="og:description" content="{escHtml Config.blogDescription}" />
    <meta property="og:image" content="{Config.blogBaseUrl}/assets/notion_avatar.png" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{escHtml Config.blogTitle}" />
    <meta name="twitter:description" content="{escHtml Config.blogDescription}" />
    <meta name="twitter:image" content="{Config.blogBaseUrl}/assets/notion_avatar.png" />"""
        let indexJsonLd = $"""<script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"WebSite","name":"{escJson Config.blogTitle}","url":"{Config.blogBaseUrl}","description":"{escJson Config.blogDescription}","author":{{"@type":"Person","name":"Cha Jinwoo"}}}}
    </script>"""
        let indexHead = headWithCanonical "" "index.html" + $"\n    {indexOgTags}\n    {indexJsonLd}"
        let frontPageHtmlContent = generateFinalHtml indexHead updatedHeader footer content highlightingScript
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
                    | None -> """<img src="assets/notion_avatar.png" alt="Default" class="post-thumbnail" />"""

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

        let updatedHeader = buildNav header gridFolders navFolders

        let content =
            $"""
        <h1>{categoryName}</h1>
        <ul class="posts-list posts-with-images">
            {postsHtml}
        </ul>
        """

        let categoryPageUrl = $"{Url.toUrlFriendly categoryName}.html"
        let categoryPageHtml = generateFinalHtml (headWithCanonical $" - {categoryName}" categoryPageUrl) updatedHeader footer content highlightingScript

        printfn $"Processing category page: {categoryName} ->"
        Disk.writeFile outputPath categoryPageHtml

    // 글 한 편을 리스트 아이템으로 렌더 (카테고리/MOC/sub_index 공용)
    let private renderPostItem (post: Post) =
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
            | None -> """<img src="assets/notion_avatar.png" alt="Default" class="post-thumbnail" />"""
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
                </li>"""

    let private renderPostList (posts: Post list) =
        posts |> List.map renderPostItem |> String.concat "\n            "

    // markdown 파일을 본문 HTML로 변환 (없으면 빈 문자열)
    let private mdFileToHtml (path: string) =
        if File.Exists(path) then
            File.ReadAllText(path)
            |> Obsidian.removeYamlFrontMatter
            |> Obsidian.convertWikiLinks path
            |> Markdown.ToHtml
        else ""

    // MOC 페이지: moc.md 본문 + 하위 leaf로 가는 링크 목록 (글 목록은 sub_index 페이지에서)
    // leafLinks: (leaf 폴더명, leaf 페이지 URL, 글 개수) 리스트
    let createMocPage (header: string) (footer: string) (categoryName: string) (mocPath: string) (leafLinks: (string * string * int) list) (loosePosts: Post list) (outputPath: string) (navFolders: string array) (gridFolders: (string * Post list) list) =
        let mocBodyHtml = mdFileToHtml mocPath

        // 하위 분야로 가는 링크 목록
        let leafLinksHtml =
            leafLinks
            |> List.map (fun (leaf, url, count) ->
                $"""
                <li class="moc-leaf-item">
                    <a href="{url}" class="moc-leaf-link">{leaf}</a>
                    <span class="moc-leaf-count">{count}편</span>
                </li>""")
            |> String.concat "\n            "

        // leaf에 안 속한 MOC 폴더 직속 글 (있을 때만 평면 목록)
        let looseHtml =
            if loosePosts.IsEmpty then ""
            else $"""
        <ul class="posts-list posts-with-images">
            {renderPostList loosePosts}
        </ul>"""

        let updatedHeader = buildNav header gridFolders navFolders

        let content =
            $"""
        <h1>{categoryName}</h1>
        <div class="moc-intro">{mocBodyHtml}</div>
        <ul class="moc-leaf-list">
            {leafLinksHtml}
        </ul>
        {looseHtml}
        """

        let mocPageUrl = $"{Url.toUrlFriendly categoryName}.html"
        let mocPageHtml = generateFinalHtml (headWithCanonical $" - {categoryName}" mocPageUrl) updatedHeader footer content highlightingScript

        printfn $"Processing MOC page: {categoryName} ->"
        Disk.writeFile outputPath mocPageHtml

    // sub_index 페이지: 상위 MOC로 돌아가는 링크 + sub_index.md 소개 + 그 폴더 글목록
    let createSubIndexPage (header: string) (footer: string) (leafName: string) (parentName: string) (parentUrl: string) (subIndexPath: string) (posts: Post list) (outputPath: string) (navFolders: string array) (gridFolders: (string * Post list) list) =
        let introHtml = mdFileToHtml subIndexPath
        let postsHtml = renderPostList posts

        let updatedHeader = buildNav header gridFolders navFolders

        let content =
            $"""
        <p class="subindex-breadcrumb"><a href="{parentUrl}">← {parentName}</a></p>
        <h1>{leafName}</h1>
        <div class="moc-intro">{introHtml}</div>
        <ul class="posts-list posts-with-images">
            {postsHtml}
        </ul>
        """

        let leafPageUrl = $"{Url.toUrlFriendly leafName}.html"
        let leafPageHtml = generateFinalHtml (headWithCanonical $" - {leafName}" leafPageUrl) updatedHeader footer content highlightingScript

        printfn $"Processing sub_index page: {leafName} ->"
        Disk.writeFile outputPath leafPageHtml

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
                    | None -> """<img src="assets/notion_avatar.png" alt="Default" class="post-thumbnail" />"""

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

        let updatedHeader = buildNav header gridFolders navFolders

        let content =
            $"""
        <h1>Posts</h1>
        <ul class="posts-list posts-with-images">
            {postsHtml}
        </ul>
        """

        let postsPageHtml = generateFinalHtml (headWithCanonical " - Posts" "posts.html") updatedHeader footer content highlightingScript

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

        let updatedHeader = buildNav header gridFolders navFolders

        let content =
            $"""
        <section class="grid-section">
            <h1 class="grid-title">{sectionTitle}</h1>
            <div class="papers-grid">
            {gridContentHtml}
            </div>
        </section>
        """

        let gridPageUrl = $"{Url.toUrlFriendly sectionTitle}.html"
        let gridPageHtml = generateFinalHtml (headWithCanonical $" - {sectionTitle}" gridPageUrl) updatedHeader footer content highlightingScript

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

        let updatedHeader = buildNav header [] navFolders

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
        let postsHtml =
            tagPosts
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
                    | None -> """<img src="assets/notion_avatar.png" alt="Default" class="post-thumbnail" />"""

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

        let content =
            $"""
        <h1>태그: {tagName}</h1>
        <p>{tagPosts.Length}개의 게시물</p>
        <ul class="posts-list posts-with-images">
            {postsHtml}
        </ul>
        """
        
        let updatedHeader = buildNav header [] navFolders
        let tagPageUrl = $"tag-{Url.toUrlFriendly tagName}.html"
        let tagPageHtml = generateFinalHtml (headWithCanonical $" - 태그: {tagName}" tagPageUrl) updatedHeader footer content ""
        
        printfn $"Processing tag page: {tagName} -> {tagPosts.Length} posts"
        Disk.writeFile outputPath tagPageHtml

    let private cdata (content: string) =
        let safeContent = content.Replace("]]>", "]]]]><![CDATA[>")
        "<![CDATA[" + safeContent + "]]>"

    let private makeFeedUrlsAbsolute (html: string) =
        let prefixAbsoluteUrl (m: Match) =
            let attr = m.Groups.["attr"].Value
            let url = m.Groups.["url"].Value
            if url.StartsWith("/") then
                $"{attr}{Config.blogBaseUrl}{url}"
            else
                $"{attr}{Config.blogBaseUrl}/{url}"

        Regex.Replace(
            html,
            "(?<attr>\\s(?:href|src)=\")(?<url>(?!https?://|mailto:|tel:|data:|#)[^\"]+)",
            MatchEvaluator(prefixAbsoluteUrl))

    let private renderRssContent (post: Post) =
        if File.Exists(post.SourcePath) then
            File.ReadAllText(post.SourcePath)
            |> Obsidian.removeYamlFrontMatter
            |> Obsidian.convertWikiLinks post.SourcePath
            |> (fun md -> Regex.Replace(md, "(?m)^#+\s", "\n<!-- -->\n$0"))
            |> Markdown.ToHtml
            |> expandArchMarkers
            |> makeFeedUrlsAbsolute
            |> cdata
        else
            cdata ""

    let private renderRssItems (posts: Post list) =
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
                | Some desc -> cdata desc
                | None -> cdata ""

            let content = renderRssContent post

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
<title>{cdata post.Title}</title>
<link>{postUrl}</link>
<guid isPermaLink="true">{postUrl}</guid>
<pubDate>{pubDate}</pubDate>

<description>{description}</description>
<content:encoded>{content}</content:encoded>{enclosureTag}
</item>"""
        )
        |> String.concat "\n"

    let private writeRssFeed (posts: Post list) (fileName: string) (channelTitle: string) (channelDescription: string) =
        let items = renderRssItems posts

        let latestBuildDate =
            posts
            |> List.choose (fun p -> p.Date)
            |> List.sortByDescending id
            |> List.tryHead
            |> Option.map (fun dt -> dt.ToUniversalTime().ToString("R"))
            |> Option.defaultValue (System.DateTime.UtcNow.ToString("R"))

        let rssXml =
            $"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
    <title>{channelTitle}</title>
    <link>{Config.blogBaseUrl}</link>
    <description>{channelDescription}</description>
    <language>ko-kr</language>
    <lastBuildDate>{latestBuildDate}</lastBuildDate>
    <atom:link href="{Config.blogBaseUrl}/{fileName}" rel="self" type="application/rss+xml" />
    {items}
</channel>
</rss>"""
        Disk.writeFile (Path.Combine(Config.outputDir, fileName)) rssXml

    let createRssFeed (posts: Post list) =
        let postsOnly = posts |> List.filter (fun p -> p.Category <> "Dictionary")
        writeRssFeed postsOnly "rss.xml" Config.blogTitle Config.blogDescription
        writeRssFeed postsOnly "rss-posts.xml" Config.blogTitle Config.blogDescription

        let gridPostsOnly = posts |> List.filter (fun p -> p.Category = "Posts")
        if not gridPostsOnly.IsEmpty then
            writeRssFeed
                gridPostsOnly
                "rss-grid-posts.xml"
                $"{Config.blogTitle} - Posts"
                "General posts feed from startedourmission."

        let gridPapersOnly = posts |> List.filter (fun p -> p.Category = "Papers")
        if not gridPapersOnly.IsEmpty then
            writeRssFeed
                gridPapersOnly
                "rss-grid-papers.xml"
                $"{Config.blogTitle} - Papers"
                "Papers feed from startedourmission."

    let private sitemapUrl (loc: string) (lastmod: string) (priority: string) =
        $"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>{priority}</priority>\n  </url>"

    let createSitemap (posts: Post list) (gridSections: (string * Post list) list) (navFolders: string array) (allTags: string list) =
        let lastmod = System.DateTime.UtcNow.ToString("yyyy-MM-dd")

        let indexEntry = sitemapUrl $"{Config.blogBaseUrl}/index.html" lastmod "1.0"
        let postsPageEntry = sitemapUrl $"{Config.blogBaseUrl}/posts.html" lastmod "0.8"

        let postEntries =
            posts
            |> List.map (fun post ->
                let postLastmod =
                    match post.Date with
                    | Some d -> d.ToString("yyyy-MM-dd")
                    | None -> lastmod
                sitemapUrl $"{Config.blogBaseUrl}/{System.Uri.EscapeUriString(post.Url)}" postLastmod "0.6")
            |> String.concat "\n"

        let gridEntries =
            gridSections
            |> List.map (fun (title, _) ->
                let url = Url.toUrlFriendly title
                sitemapUrl $"{Config.blogBaseUrl}/{url}.html" lastmod "0.7")
            |> String.concat "\n"

        let navEntries =
            navFolders
            |> Array.map (fun folderName ->
                let url = Url.toUrlFriendly folderName
                sitemapUrl $"{Config.blogBaseUrl}/{url}.html" lastmod "0.7")
            |> String.concat "\n"

        let tagEntries =
            allTags
            |> List.map (fun tag ->
                let url = Url.toUrlFriendly tag
                sitemapUrl $"{Config.blogBaseUrl}/tag-{url}.html" lastmod "0.4")
            |> String.concat "\n"

        let sitemapXml =
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            + "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
            + indexEntry + "\n"
            + postsPageEntry + "\n"
            + postEntries + "\n"
            + gridEntries + "\n"
            + navEntries + "\n"
            + tagEntries + "\n"
            + "</urlset>"
        let sitemapPath = Path.Combine(Config.outputDir, "sitemap.xml")
        Disk.writeFile sitemapPath sitemapXml

    let createRobotsTxt () =
        let content =
            "User-agent: *\n"
            + "Allow: /\n\n"
            + "# AI Crawlers\n"
            + "User-agent: GPTBot\n"
            + "Allow: /\n\n"
            + "User-agent: anthropic-ai\n"
            + "Allow: /\n\n"
            + "User-agent: ClaudeBot\n"
            + "Allow: /\n\n"
            + "User-agent: CCBot\n"
            + "Allow: /\n\n"
            + "User-agent: Google-Extended\n"
            + "Allow: /\n\n"
            + "Sitemap: " + Config.blogBaseUrl + "/sitemap.xml\n"
        let robotsPath = Path.Combine(Config.outputDir, "robots.txt")
        Disk.writeFile robotsPath content

    let createLlmsTxt (posts: Post list) (gridSections: (string * Post list) list) =
        let postsList =
            posts
            |> List.map (fun post ->
                let desc =
                    match post.Description with
                    | Some d -> ": " + d
                    | None -> ""
                let tags =
                    if post.Tags.IsEmpty then ""
                    else " [" + (post.Tags |> String.concat ", ") + "]"
                $"- [{post.Title}]({Config.blogBaseUrl}/{System.Uri.EscapeUriString(post.Url)}){desc}{tags}")
            |> String.concat "\n"

        let gridSectionsList =
            gridSections
            |> List.map (fun (title, sectionPosts) ->
                let header = $"### {title}\n"
                let items =
                    sectionPosts
                    |> List.map (fun post ->
                        $"- [{post.Title}]({Config.blogBaseUrl}/{System.Uri.EscapeUriString(post.Url)})")
                    |> String.concat "\n"
                header + items)
            |> String.concat "\n\n"

        let content =
            "# " + Config.blogTitle + "\n\n"
            + "> " + Config.blogDescription + "\n\n"
            + "- Author: Cha Jinwoo\n"
            + "- URL: " + Config.blogBaseUrl + "\n"
            + "- RSS: " + Config.blogBaseUrl + "/rss.xml\n"
            + "- Language: ko\n\n"
            + "## Posts\n\n"
            + postsList + "\n\n"
            + (if gridSectionsList.Length > 0 then "## Collections\n\n" + gridSectionsList + "\n" else "")
        let llmsPath = Path.Combine(Config.outputDir, "llms.txt")
        Disk.writeFile llmsPath content
