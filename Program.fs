open System.IO
open SkunkUtils
open SkunkHtml

[<EntryPoint>]
let main argv =
    argv |> ignore

    if not (Directory.Exists(Config.markdownDir)) then
        printfn $"Markdown directory does not exist : {Config.markdownDir}"
        failwith "Markdown directory not found"

    if not (Directory.Exists(Config.outputDir)) then
        printfn $"Creating {Path.GetFileName Config.outputDir} folder"
        Directory.CreateDirectory(Config.outputDir)
        |> ignore

    let header = Disk.readFile (Path.Combine(Config.htmlDir, "header.html"))
    let footer = Disk.readFile (Path.Combine(Config.htmlDir, "footer.html"))

    // frontPage를 제외한 모든 마크다운 파일을 블로그 글로 처리 (하위 폴더 포함)
    let allMarkdownFiles = Directory.GetFiles(Config.markdownDir, "*.md", SearchOption.AllDirectories)
    
    // 모든 Canvas 파일 찾기
    let allCanvasFiles = Directory.GetFiles(Config.markdownDir, "*.canvas", SearchOption.AllDirectories)

    // 인덱스 페이지의 글 목록에 표시될 파일들
    let indexListFiles =
        allMarkdownFiles
        |> Array.filter (fun file -> 
            // 특수 파일 목록에 없는 파일만 목록에 표시
            not (Config.specialFiles |> List.contains (Path.GetFileName(file))))
            
    // 모든 블로그 글로 처리할 파일들 (인덱스 및 MOC 특수 파일 제외)
    // moc.md / sub_index.md는 개별 해시 페이지로 만들지 않고 MOC 카테고리 페이지로만 렌더
    let blogArticleFiles =
        allMarkdownFiles
        |> Array.filter (fun file ->
            let name = Path.GetFileName(file)
            name <> Config.frontPageMarkdownFileName &&
            name <> Config.mocFileName &&
            name <> Config.subIndexFileName)

    // 모든 폴더들 찾기
    let allFolders = Directory.GetDirectories(Config.markdownDir)
    
    // grid_ 폴더들 찾기
    let gridFolders =
        allFolders
        |> Array.filter (fun dir -> 
            let folderName = Path.GetFileName(dir)
            folderName.StartsWith("grid_"))
        |> Array.map (fun dir ->
            let folderName = Path.GetFileName(dir)
            let gridTitle = folderName.Substring(5) // "grid_" 제거
            (dir, gridTitle))

    // 내비게이션용 폴더들 (grid_가 아니고 특수 폴더가 아닌 것들, Config 순서대로 정렬)
    let navFoldersUnordered =
        allFolders
        |> Array.filter (fun dir -> 
            let folderName = Path.GetFileName(dir)
            not (folderName.StartsWith("grid_")) && 
            not (folderName.StartsWith(".")) &&  // 숨김 폴더 제외
            folderName <> "_assets" &&
            folderName <> "assets")
        |> Array.map (fun dir -> Path.GetFileName(dir))
    
    let navFolders =
        // Config 순서대로 정렬
        let orderedNav = 
            Config.navSectionOrder
            |> List.filter (fun name -> Array.contains name navFoldersUnordered)
        
        // Config에 없는 폴더들은 맨 뒤에 알파벳 순으로 추가
        let remainingNav = 
            navFoldersUnordered
            |> Array.filter (fun name -> not (List.contains name Config.navSectionOrder))
            |> Array.sort
            |> Array.toList
        
        (orderedNav @ remainingNav) |> List.toArray

    // 모든 게시물 정보 수집 및 폴더별 분류
    let allPosts =
        indexListFiles  // 특수 파일이 제외된 목록 사용
        |> Array.map (fun file ->
            let content = File.ReadAllText(file)
            let filename = Path.GetFileNameWithoutExtension(file)
            let hashId = Url.toHashId filename
            let imageUrl = Obsidian.extractImageUrl file content
            let dateValue = Obsidian.extractDate content filename
            let summary = Obsidian.extractSummary content
            let description = Obsidian.extractDescription content
            let tags = Obsidian.extractTags content
            let buzz = Obsidian.extractBuzz content

            // 파일이 어떤 폴더에 속하는지 확인
            let category =
                // 먼저 grid 폴더 확인
                match gridFolders |> Array.tryFind (fun (folderPath, _) -> file.StartsWith(folderPath)) with
                | Some (_, title) -> title
                | None ->
                    // grid 폴더가 아니면 nav 폴더 확인 (MOC 폴더는 하위 글도 StartsWith로 부모에 귀속됨)
                    match navFolders |> Array.tryFind (fun folderName ->
                        let folderPath = Path.Combine(Config.markdownDir, folderName)
                        file.StartsWith(folderPath)) with
                    | Some folderName -> folderName
                    | None -> "Posts" // 어떤 폴더에도 속하지 않으면 Posts

            // 직속 폴더명이 category(부모 MOC/카테고리)와 다르면 leaf 하위 폴더 (그룹핑용)
            let subCategory =
                let immediateFolder = Path.GetFileName(Path.GetDirectoryName(file))
                if immediateFolder = category then None
                else Some immediateFolder

            {
                Title = filename
                Url = $"{hashId}.html"
                SourcePath = file
                ImageUrl = imageUrl
                Category = category
                SubCategory = subCategory
                Date = dateValue
                Summary = summary
                Description = description
                Tags = tags
                Buzz = buzz
            })
        |> Array.sortByDescending (fun post -> post.Date)
        |> Array.toList

    // 폴더별로 게시물 그룹화 (Config 순서대로 정렬)
    let gridSections =
        let sectionMap = 
            gridFolders
            |> Array.map (fun (_, title) ->
                let posts = allPosts |> List.filter (fun post -> post.Category = title)
                (title, posts))
            |> Map.ofArray
        
        // Config 순서대로 섹션 생성
        let orderedSections = 
            Config.gridSectionOrder
            |> List.choose (fun title -> 
                Map.tryFind title sectionMap
                |> Option.map (fun posts -> (title, posts)))
        
        // Config에 없는 섹션들은 맨 뒤에 알파벳 순으로 추가
        let remainingSections = 
            sectionMap
            |> Map.toList
            |> List.filter (fun (title, _) -> not (List.contains title Config.gridSectionOrder))
            |> List.sortBy fst
        
        orderedSections @ remainingSections

    // grid_Posts 폴더의 글들을 Posts 페이지로 사용
    let regularPosts = allPosts |> List.filter (fun post -> post.Category = "Posts")

    // Canvas 파일들을 파싱하여 Canvas 객체 리스트 생성
    let allCanvases =
        allCanvasFiles
        |> Array.map CanvasParser.parseCanvas
        |> Array.toList

    // 디버깅 정보 출력
    let navFoldersStr = String.concat ", " navFolders
    printfn $"Total posts: {allPosts.Length}"
    printfn $"Nav folders: {navFoldersStr}"
    printfn $"Grid sections: {gridSections.Length}"
    printfn $"Regular posts: {regularPosts.Length}"
    printfn $"Canvas files: {allCanvases.Length}"

    let createBlogArticlePages () = 
        blogArticleFiles
        |> Array.iter (createPage header footer)

    let createCategoryPages () =
        navFolders
        |> Array.iter (fun folderName ->
            let categoryPosts = allPosts |> List.filter (fun post -> post.Category = folderName)
            printfn $"Category: {folderName}, Posts count: {categoryPosts.Length}"
            categoryPosts |> List.iter (fun post -> printfn $"  - {post.Title}")
            let categoryPagePath = Path.Combine(Config.outputDir, $"{Url.toUrlFriendly folderName}.html")

            // MOC 폴더(moc.md 보유)면 MOC 페이지(leaf 링크 목록), 아니면 일반 카테고리 페이지
            // 본문 markdown→html 변환은 SkunkHtml 함수 안에서 처리(Markdig 의존을 Program.fs에 두지 않음)
            let mocPath = Path.Combine(Config.markdownDir, folderName, Config.mocFileName)
            if File.Exists(mocPath) then
                // 하위 leaf 폴더 순서(알파벳) + URL + sub_index 경로 + 그 폴더 글목록
                let leafGroups =
                    Directory.GetDirectories(Path.Combine(Config.markdownDir, folderName))
                    |> Array.map Path.GetFileName
                    |> Array.filter (fun n -> n <> "_assets" && not (n.StartsWith(".")))
                    |> Array.sort
                    |> Array.toList
                    |> List.map (fun leaf ->
                        let subIndexPath = Path.Combine(Config.markdownDir, folderName, leaf, Config.subIndexFileName)
                        let leafUrl = $"{Url.toUrlFriendly leaf}.html"
                        let leafPosts =
                            categoryPosts |> List.filter (fun post -> post.SubCategory = Some leaf)
                        (leaf, leafUrl, subIndexPath, leafPosts))

                // leaf에 속하지 않은(=MOC 폴더 직속) 글들
                let loosePosts =
                    categoryPosts |> List.filter (fun post -> post.SubCategory.IsNone)

                // MOC 페이지: moc 본문 + leaf 링크 목록(+직속 글)
                let mocLeafLinks =
                    leafGroups |> List.map (fun (leaf, url, _, posts) -> (leaf, url, posts.Length))
                SkunkHtml.createMocPage header footer folderName mocPath mocLeafLinks loosePosts categoryPagePath navFolders gridSections

                // 각 leaf의 sub_index 페이지: 소개 + 그 폴더 글목록 (상위 MOC로 돌아가는 링크 포함)
                let mocUrl = $"{Url.toUrlFriendly folderName}.html"
                leafGroups
                |> List.iter (fun (leaf, leafUrl, subIndexPath, leafPosts) ->
                    let leafPagePath = Path.Combine(Config.outputDir, leafUrl)
                    SkunkHtml.createSubIndexPage header footer leaf folderName mocUrl subIndexPath leafPosts leafPagePath navFolders gridSections)
            else
                SkunkHtml.createCategoryPage header footer folderName categoryPosts categoryPagePath navFolders gridSections)
    
    let createCanvasPages () = 
        allCanvases
        |> List.iter (fun canvas ->
            printfn $"Canvas: {canvas.Title}, Nodes: {canvas.Nodes.Length}, Edges: {canvas.Edges.Length}"
            let canvasPagePath = Path.Combine(Config.outputDir, canvas.Url)
            SkunkHtml.createCanvasPage header footer canvas canvasPagePath navFolders)
    
    let createTagPages () =
        // 모든 태그 수집
        let allTags = 
            allPosts
            |> List.collect (fun post -> post.Tags)
            |> List.distinct
            |> List.sort
        
        // 태그별 페이지 생성
        allTags
        |> List.iter (fun tag ->
            let tagPosts = allPosts |> List.filter (fun post -> List.contains tag post.Tags)
            let tagUrl = Url.toUrlFriendly tag
            let tagPagePath = Path.Combine(Config.outputDir, $"tag-{tagUrl}.html")
            
            SkunkHtml.createTagPage header footer tag tagPosts tagPagePath navFolders)

    // 인덱스 페이지를 제외한 모든 마크다운을 처리하므로, 이제 그외 페이지 처리는 필요없음
    let createOtherPages () =
        () // 모든 마크다운 파일이 블로그 글로 처리되므로 필요없음

    let createPostsAndGridPages () =
        // Posts 페이지 생성 (grid_Posts 폴더의 글들을 리스트 형식으로)
        let postsPagePath = Path.Combine(Config.outputDir, "posts.html")
        SkunkHtml.createPostsPage header footer regularPosts postsPagePath navFolders gridSections

        // Grid 섹션 페이지들 생성 (Posts는 위에서 별도 처리)
        gridSections
        |> List.filter (fun (title, _) -> title <> "Posts")
        |> List.iter (fun (title, posts) ->
            let urlFriendlyTitle = Url.toUrlFriendly title
            let gridPagePath = Path.Combine(Config.outputDir, $"{urlFriendlyTitle}.html")
            SkunkHtml.createGridSectionPage header footer title posts gridPagePath navFolders gridSections)

    createIndexPage header footer gridSections navFolders regularPosts allPosts
    createOtherPages ()
    createBlogArticlePages ()
    createCategoryPages ()
    createCanvasPages ()
    createTagPages ()
    createPostsAndGridPages ()
    SkunkHtml.createTrendsPage header footer navFolders gridSections
    SkunkHtml.createRoadmapPage header footer navFolders gridSections
    SkunkHtml.createRssFeed allPosts

    // SEO + GEO 파일 생성
    let allTags =
        allPosts
        |> List.collect (fun post -> post.Tags)
        |> List.distinct
        |> List.sort
    SkunkHtml.createSitemap allPosts gridSections navFolders allTags
    SkunkHtml.createRobotsTxt ()
    SkunkHtml.createLlmsTxt allPosts gridSections

    // Copy ads.txt to output
    let adsTxtSource = Path.Combine(Config.sourceDir, "ads.txt")
    let adsTxtDest = Path.Combine(Config.outputDir, "ads.txt")
    if File.Exists(adsTxtSource) then
        File.Copy(adsTxtSource, adsTxtDest, true)
        printfn "Copied ads.txt to output"

    Disk.copyFolderToOutput Config.fontsDir Config.outputFontsDir
    Disk.copyFolderToOutput Config.cssDir Config.outputCssDir
    Disk.copyFolderToOutput Config.imagesDir Config.outputImagesDir
    Disk.copyFolderToOutput Config.assetsDir Config.outputAssetsDir
    Disk.copyFolderToOutput Config.scriptsDir Config.outputScriptsDir

    // 모든 깊이의 _assets 폴더를 복사 (중첩 MOC 구조 지원)
    // 이미지 URL prefix는 글의 직속 폴더명을 쓰므로(getAssetsPrefix), 출력도 직속 폴더명 기준으로 복사
    Directory.GetDirectories(Config.markdownDir, "_assets", SearchOption.AllDirectories)
    |> Array.iter (fun subAssetsDir ->
        let parentFolder = Path.GetFileName(Path.GetDirectoryName(subAssetsDir))
        // 루트(_assets)는 위에서 imagesDir로 이미 복사됨 → 건너뜀
        if parentFolder <> Path.GetFileName(Config.markdownDir) then
            let urlFriendlyFolder = Url.toUrlFriendly parentFolder
            let outputSubAssetsDir = Path.Combine(Config.outputDir, urlFriendlyFolder, "_assets")
            Disk.copyFolderToOutput subAssetsDir outputSubAssetsDir)

    printf "\nBuild complete. Your site is ready for deployment!"
    0
