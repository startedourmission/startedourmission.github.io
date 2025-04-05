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

    let allMarkdownFiles = Directory.GetFiles(Config.markdownDir, "*.md")

    let blogArticleFiles =
        allMarkdownFiles
        |> Array.filter isArticle

    let listOfAllBlogArticles =
        blogArticleFiles
        |> Array.map (fun file ->
            let date = Path.GetFileNameWithoutExtension(file)
            let title = extractTitleFromMarkdownFile(file)
            // 제목에서 앞부분 숫자 제거 후 URL 친화적으로 변환
            let cleanTitle = Obsidian.removeLeadingNumbers title
            let urlFriendlyTitle = Url.toUrlFriendly cleanTitle
            (date, title, $"{urlFriendlyTitle}.html"))
        |> Array.sortByDescending (fun (date, _, _) -> date)
        |> Array.toList

    let createBlogArticlePages () =
        blogArticleFiles
        |> Array.iter (createPage header footer)

    let createOtherPages () =
        allMarkdownFiles
        |> Array.filter (fun file -> not (isArticle file))
        |> Array.filter (fun file -> Path.GetFileName(file) <> Config.frontPageMarkdownFileName)
        |> Array.iter (createPage header footer)

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
