module SkunkUtils

module Config =
    open System.IO

    let sourceDir = __SOURCE_DIRECTORY__

    let markdownDir = Path.Combine(sourceDir, "markdown-blog")
    let htmlDir = Path.Combine(sourceDir, "html")
    let outputDir = Path.Combine(sourceDir, "skunk-html-output")

    let cssDir = Path.Combine(sourceDir, "css")
    let outputCssDir = Path.Combine(outputDir, "css")

    let fontsDir = Path.Combine(sourceDir, "fonts")
    let outputFontsDir = Path.Combine(outputDir, "fonts")

    let imagesDir = Path.Combine(markdownDir, "images")
    let outputImagesDir = Path.Combine(outputDir, "images")

    let assetsDir = Path.Combine(sourceDir, "assets")
    let outputAssetsDir = Path.Combine(outputDir, "assets")

    let scriptsDir = Path.Combine(sourceDir, "scripts")
    let outputScriptsDir = Path.Combine(outputDir, "scripts")

    let frontPageMarkdownFileName = "index.md"
    
    // 인덱스 페이지에 표시하지 않을 특수 파일들
    let specialFiles = [frontPageMarkdownFileName; "links.md"]

module Disk =
    open System.IO

    let readFile (path: string) =
        path
        |> File.Exists
        |> function
            | true -> File.ReadAllText(path)
            | false -> ""

    let writeFile (path: string) (content: string) =
        File.WriteAllText(path, content)
        printfn $"Generated: {Path.GetFileName path} -> {path}\n"

    let copyFolderToOutput (sourceFolder: string) (destinationFolder: string) =
        if not (Directory.Exists(sourceFolder)) then
            printfn $"Source folder does not exist: {sourceFolder}"
        else
            if not (Directory.Exists(destinationFolder)) then
                Directory.CreateDirectory(destinationFolder)
                |> ignore

            Directory.GetFiles(sourceFolder)
            |> Array.iter (fun file ->
                let fileName = Path.GetFileName(file)
                let destFile = Path.Combine(destinationFolder, fileName)
                printfn $"Copying: {fileName} -> {destFile}"
                File.Copy(file, destFile, true))

module Url =
    open System.Text.RegularExpressions

    let toUrlFriendly (input: string) =
        input.ToLowerInvariant()
        |> fun text -> Regex.Replace(text, @"[^\w\s]", "") // Remove all non-alphanumeric characters
        |> fun text -> Regex.Replace(text, @"\s+", "-") // Replace spaces with hyphens

module Obsidian =
    open System.Text.RegularExpressions

    // Obsidian 링크를 HTML 링크로 변환하는 함수
    let convertWikiLinks (markdownContent: string) =
        let wikiLinkPattern = @"\[\[(.*?)\]\]"
        
        // 정규식으로 Obsidian 스타일 링크 찾기
        let regex = Regex(wikiLinkPattern)
        
        // 각 매치를 HTML 링크로 변환
        regex.Replace(markdownContent, fun m ->
            let linkText = m.Groups.[1].Value
            
            // 링크 텍스트에 파이프(|)가 있으면 표시 텍스트와 대상을 분리
            if linkText.Contains("|") then
                let parts = linkText.Split('|')
                let target = parts.[0].Trim()
                let displayText = parts.[1].Trim()
                
                // 파일명을 URL 친화적으로 변환
                let urlFriendlyTarget = Url.toUrlFriendly target
                
                $"[{displayText}]({urlFriendlyTarget}.html)"
            else
                // 파이프가 없으면 링크 텍스트가 대상이자 표시 텍스트
                // 파일명을 URL 친화적으로 변환
                let urlFriendlyTarget = Url.toUrlFriendly linkText
                
                $"[{linkText}]({urlFriendlyTarget}.html)"
        )
        
    // YAML 프론트매터에서 태그 추출
    let extractTags (markdownContent: string) =
        let frontMatterPattern = @"^\s*---\s*\n([\s\S]*?)\n\s*---\s*\n"
        let frontMatterMatch = Regex.Match(markdownContent, frontMatterPattern)
        
        if frontMatterMatch.Success then
            let yamlContent = frontMatterMatch.Groups.[1].Value
            let tagPattern = @"tags:\s*\n((?:\s*-\s*[^\n]+\n?)*)"
            let tagMatch = Regex.Match(yamlContent, tagPattern)
            
            if tagMatch.Success then
                let tagLines = tagMatch.Groups.[1].Value
                let individualTagPattern = @"-\s*([^\n]+)"
                let tags = Regex.Matches(tagLines, individualTagPattern)
                           |> Seq.cast<Match>
                           |> Seq.map (fun m -> m.Groups.[1].Value.Trim())
                           |> Seq.toList
                tags
            else
                []
        else
            []
    
    // YAML 프론트매터에서 이미지 URL 추출
    let extractImageUrl (markdownContent: string) =
        let frontMatterPattern = @"^\s*---\s*\n([\s\S]*?)\n\s*---\s*\n"
        let frontMatterMatch = Regex.Match(markdownContent, frontMatterPattern)
        
        if frontMatterMatch.Success then
            let yamlContent = frontMatterMatch.Groups.[1].Value
            let imagePattern = @"image:\s*(.+)"
            let imageMatch = Regex.Match(yamlContent, imagePattern)
            
            if imageMatch.Success then
                Some (imageMatch.Groups.[1].Value.Trim())
            else
                None
        else
            None
    
    // Obsidian 프로퍼티 영역 제거 (---로 둘러싸인 YAML 프론트매터)
    let removeYamlFrontMatter (markdownContent: string) =
        let frontMatterPattern = @"^\s*---\s*\n[\s\S]*?\n\s*---\s*\n"
        Regex.Replace(markdownContent, frontMatterPattern, "")