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

    let blogArticleFiles =
        allMarkdownFiles
        |> Array.filter (fun file -> Path.GetFileName(file) <> Config.frontPageMarkdownFileName)

    let listOfAllBlogArticles =
        blogArticleFiles
        |> Array.map (fun file ->
            // 파일명이 제목이자 표시명이 됨
            let filename = Path.GetFileNameWithoutExtension(file)
            // 파일명을 URL 친화적으로 변환
            let urlFriendlyTitle = Url.toUrlFriendly filename
            (filename, filename, $"{urlFriendlyTitle}.html"))
        |> Array.sortByDescending (fun (date, _, _) -> date)
        |> Array.toList

    let createBlogArticlePages () =
        blogArticleFiles
        |> Array.iter (createPage header footer)

    // 인덱스 페이지를 제외한 모든 마크다운을 처리하므로, 이제 그외 페이지 처리는 필요없음
    let createOtherPages () =
        () // 모든 마크다운 파일이 블로그 글로 처리되므로 필요없음

    createIndexPage header footer listOfAllBlogArticles
    createOtherPages ()
    createBlogArticlePages ()


    Disk.copyFolderToOutput Config.fontsDir Config.outputFontsDir
    Disk.copyFolderToOutput Config.cssDir Config.outputCssDir
    Disk.copyFolderToOutput Config.imagesDir Config.outputImagesDir
    Disk.copyFolderToOutput Config.assetsDir Config.outputAssetsDir
    Disk.copyFolderToOutput Config.scriptsDir Config.outputScriptsDir

    printf "\nBuild complete. Your site is ready for deployment!"
    0
