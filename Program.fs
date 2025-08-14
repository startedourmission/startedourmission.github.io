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

    // 내비게이션용 폴더들 (grid_가 아니고 특수 폴더가 아닌 것들)
    let navFolders =
        allFolders
        |> Array.filter (fun dir -> 
            let folderName = Path.GetFileName(dir)
            not (folderName.StartsWith("grid_")) && 
            not (folderName.StartsWith(".")) &&  // 숨김 폴더 제외
            folderName <> "images" && 
            folderName <> "assets")
        |> Array.map (fun dir -> Path.GetFileName(dir))

    // 모든 게시물 정보 수집 및 폴더별 분류
    let allPosts =
        indexListFiles  // 특수 파일이 제외된 목록 사용
        |> Array.map (fun file ->
            let content = File.ReadAllText(file)
            let filename = Path.GetFileNameWithoutExtension(file)
            let urlFriendlyTitle = Url.toUrlFriendly filename
            let imageUrl = Obsidian.extractImageUrl content
            
            // 파일이 어떤 grid 폴더에 속하는지 확인
            let category = 
                gridFolders
                |> Array.tryFind (fun (folderPath, _) -> file.StartsWith(folderPath))
                |> Option.map (fun (_, title) -> title)
                |> Option.defaultValue "Posts"
            
            {
                Title = filename
                Url = $"{urlFriendlyTitle}.html"
                ImageUrl = imageUrl
                Category = category
            })
        |> Array.sortByDescending (fun post -> post.Title)
        |> Array.toList

    // 폴더별로 게시물 그룹화
    let gridSections =
        gridFolders
        |> Array.map (fun (_, title) ->
            let posts = allPosts |> List.filter (fun post -> post.Category = title)
            (title, posts))
        |> Array.toList

    let regularPosts = allPosts |> List.filter (fun post -> post.Category = "Posts")

    let createBlogArticlePages () =
        blogArticleFiles
        |> Array.iter (createPage header footer)

    let createCategoryPages () =
        navFolders
        |> Array.iter (fun folderName ->
            let categoryPosts = allPosts |> List.filter (fun post -> post.Category = folderName)
            let categoryPagePath = Path.Combine(Config.outputDir, $"{Url.toUrlFriendly folderName}.html")
            SkunkHtml.createCategoryPage header footer folderName categoryPosts categoryPagePath navFolders)

    // 인덱스 페이지를 제외한 모든 마크다운을 처리하므로, 이제 그외 페이지 처리는 필요없음
    let createOtherPages () =
        () // 모든 마크다운 파일이 블로그 글로 처리되므로 필요없음

    createIndexPage header footer gridSections navFolders
    createOtherPages ()
    createBlogArticlePages ()
    createCategoryPages ()


    Disk.copyFolderToOutput Config.fontsDir Config.outputFontsDir
    Disk.copyFolderToOutput Config.cssDir Config.outputCssDir
    Disk.copyFolderToOutput Config.imagesDir Config.outputImagesDir
    Disk.copyFolderToOutput Config.assetsDir Config.outputAssetsDir
    Disk.copyFolderToOutput Config.scriptsDir Config.outputScriptsDir

    printf "\nBuild complete. Your site is ready for deployment!"
    0
