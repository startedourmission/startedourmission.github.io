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
            
    // 모든 블로그 글로 처리할 파일들 (인덱스 페이지 제외)
    let blogArticleFiles =
        allMarkdownFiles
        |> Array.filter (fun file -> Path.GetFileName(file) <> Config.frontPageMarkdownFileName)

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
            folderName <> "images" && 
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
            let urlFriendlyTitle = Url.toUrlFriendly filename
            let imageUrl = Obsidian.extractImageUrl content
            let dateValue = Obsidian.extractDate content filename
            let summary = Obsidian.extractSummary content
            let description = Obsidian.extractDescription content
            let tags = Obsidian.extractTags content
            
            // 파일이 어떤 폴더에 속하는지 확인
            let category = 
                // 먼저 grid 폴더 확인
                match gridFolders |> Array.tryFind (fun (folderPath, _) -> file.StartsWith(folderPath)) with
                | Some (_, title) -> title
                | None ->
                    // grid 폴더가 아니면 nav 폴더 확인
                    match navFolders |> Array.tryFind (fun folderName -> 
                        let folderPath = Path.Combine(Config.markdownDir, folderName)
                        file.StartsWith(folderPath)) with
                    | Some folderName -> folderName
                    | None -> "Posts" // 어떤 폴더에도 속하지 않으면 Posts
            
            {
                Title = filename
                Url = $"{urlFriendlyTitle}.html"
                ImageUrl = imageUrl
                Category = category
                Date = dateValue
                Summary = summary
                Description = description
                Tags = tags
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
            SkunkHtml.createCategoryPage header footer folderName categoryPosts categoryPagePath navFolders)
    
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
            let tagPagePath = Path.Combine(Config.outputDir, "tag", $"{tagUrl}.html")
            
            // tag 디렉토리가 없으면 생성
            let tagDir = Path.GetDirectoryName(tagPagePath)
            if not (Directory.Exists(tagDir)) then
                Directory.CreateDirectory(tagDir) |> ignore
            
            SkunkHtml.createTagPage header footer tag tagPosts tagPagePath navFolders)

    // 인덱스 페이지를 제외한 모든 마크다운을 처리하므로, 이제 그외 페이지 처리는 필요없음
    let createOtherPages () = 
        () // 모든 마크다운 파일이 블로그 글로 처리되므로 필요없음

    createIndexPage header footer gridSections navFolders regularPosts
    createOtherPages ()
    createBlogArticlePages ()
    createCategoryPages ()
    createCanvasPages ()
    createTagPages ()
    SkunkHtml.createRssFeed allPosts


    Disk.copyFolderToOutput Config.fontsDir Config.outputFontsDir
    Disk.copyFolderToOutput Config.cssDir Config.outputCssDir
    Disk.copyFolderToOutput Config.imagesDir Config.outputImagesDir
    Disk.copyFolderToOutput Config.assetsDir Config.outputAssetsDir
    Disk.copyFolderToOutput Config.scriptsDir Config.outputScriptsDir

    printf "\nBuild complete. Your site is ready for deployment!"
    0