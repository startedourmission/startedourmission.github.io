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

    // frontPage를 제외한 모든 마크다운 파일을 블로그 글로 처리
    let allMarkdownFiles = Directory.GetFiles(Config.markdownDir, "*.md")

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

    let listOfAllBlogArticles =
        indexListFiles  // 특수 파일이 제외된 목록 사용
        |> Array.map (fun file ->
            // 파일명이 제목이자 표시명이 됨
            let filename = Path.GetFileNameWithoutExtension(file)
            // 파일명을 URL 친화적으로 변환
            let urlFriendlyTitle = Url.toUrlFriendly filename
            (filename, filename, $"{urlFriendlyTitle}.html"))
        |> Array.sortByDescending (fun (date, _, _) -> date)
        |> Array.toList

    let paperArticles =
        indexListFiles
        |> Array.choose (fun file ->
            let content = File.ReadAllText(file)
            let tags = Obsidian.extractTags content
            if tags |> List.contains "논문" then
                let filename = Path.GetFileNameWithoutExtension(file)
                let urlFriendlyTitle = Url.toUrlFriendly filename
                Some (filename, filename, $"{urlFriendlyTitle}.html")
            else
                None)
        |> Array.sortByDescending (fun (date, _, _) -> date)
        |> Array.toList

    let createBlogArticlePages () =
        blogArticleFiles
        |> Array.iter (createPage header footer)

    // 인덱스 페이지를 제외한 모든 마크다운을 처리하므로, 이제 그외 페이지 처리는 필요없음
    let createOtherPages () =
        () // 모든 마크다운 파일이 블로그 글로 처리되므로 필요없음

    createIndexPage header footer listOfAllBlogArticles paperArticles
    createOtherPages ()
    createBlogArticlePages ()


    Disk.copyFolderToOutput Config.fontsDir Config.outputFontsDir
    Disk.copyFolderToOutput Config.cssDir Config.outputCssDir
    Disk.copyFolderToOutput Config.imagesDir Config.outputImagesDir
    Disk.copyFolderToOutput Config.assetsDir Config.outputAssetsDir
    Disk.copyFolderToOutput Config.scriptsDir Config.outputScriptsDir

    printf "\nBuild complete. Your site is ready for deployment!"
    0
