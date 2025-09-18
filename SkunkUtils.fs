module SkunkUtils

type Post = {
    Title: string
    Url: string
    ImageUrl: string option
    Category: string
    Date: System.DateTime option
    Summary: string option
}

type CanvasNode = {
    Id: string
    Type: string
    Text: string option
    File: string option
    X: int
    Y: int
    Width: int
    Height: int
}

type CanvasEdge = {
    Id: string
    FromNode: string
    ToNode: string
    FromSide: string option
    ToSide: string option
}

type Canvas = {
    Title: string
    Url: string
    Nodes: CanvasNode list
    Edges: CanvasEdge list
}

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
    
    // 그리드 섹션 순서 설정
    let gridSectionOrder = ["BookReview"; "Papers"; "Portfolio"]
    
    // 내비게이션 섹션 순서 설정
    let navSectionOrder = ["LLM"]

    // RSS 피드 정보
    let blogTitle = "startedourmission"
    let blogDescription = "Papers, Books, and Projects that started our mission."
    let blogBaseUrl = "https://startedourmission.github.io" // 실제 배포된 블로그의 URL로 변경해야 합니다.

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
        let wikiLinkPattern = @"(!?)`\[\[(.*?)\]\]" // 이미지 링크(!)와 일반 링크를 모두 처리
        
        let regex = Regex(wikiLinkPattern)
        
        regex.Replace(markdownContent, fun m ->
            let isImage = m.Groups.[1].Value = "!"
            let linkContent = m.Groups.[2].Value

            if isImage then
                // 이미지 링크 처리 ![[image.png]]
                let imageName = linkContent
                // 모든 이미지는 'images' 폴더에 있다고 가정
                let imageUrl = $"images/{imageName}"
                // URL 인코딩 처리 (공백 등)
                let encodedUrl = System.Uri.EscapeUriString(imageUrl)
                $"<img src=\"{encodedUrl}\" alt=\"{imageName}\" class=\"embedded-image\">"
            else
                // 페이지 링크 처리 [[Page Name]] or [[Page Name|Display Text]]
                let linkText = linkContent
                if linkText.Contains("|") then
                    let parts = linkText.Split('|')
                    let target = parts.[0].Trim()
                    let displayText = parts.[1].Trim()
                    let urlFriendlyTarget = Url.toUrlFriendly target
                    $"[{displayText}]({urlFriendlyTarget}.html)"
                else
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
                let imageValue = imageMatch.Groups.[1].Value.Trim()

                // 옵시디언 이미지 링크 형식 ![[image.png]] 확인
                let wikiImagePattern = @"!\[\[(.*?)\]\]"
                let wikiMatch = Regex.Match(imageValue, wikiImagePattern)

                if wikiMatch.Success then
                    // 옵시디언 링크 형식이면, 경로를 'images/'로 구성
                    let imageName = wikiMatch.Groups.[1].Value
                    Some ($"images/{imageName}")
                else
                    // 일반 경로 형식이면, 그대로 사용
                    Some imageValue
            else
                None
        else
            None

    
    // Obsidian 프로퍼티 영역 제거 (---로 둘러싸인 YAML 프론트매터)
    let removeYamlFrontMatter (markdownContent: string) =
        let frontMatterPattern = @"^\s*---\s*\n[\s\S]*?\n\s*---\s*\n"
        Regex.Replace(markdownContent, frontMatterPattern, "")

    // YAML 프론트매터에서 날짜 추출
    let extractDate (markdownContent: string) (fileName: string) =
        // 먼저 YAML 프론트매터에서 날짜를 찾아보기
        let frontMatterPattern = @"^\s*---\s*\n([\s\S]*?)\n\s*---\s*\n"
        let frontMatterMatch = Regex.Match(markdownContent, frontMatterPattern)
        
        if frontMatterMatch.Success then
            let yamlContent = frontMatterMatch.Groups.[1].Value
            let datePattern = @"date:\s*(.+)"
            let dateMatch = Regex.Match(yamlContent, datePattern)
            
            if dateMatch.Success then
                let dateStr = dateMatch.Groups.[1].Value.Trim()
                match System.DateTime.TryParse(dateStr) with
                | true, date -> Some date
                | false, _ -> None
            else
                None
        else
            // YAML 프론트매터에 날짜가 없으면 파일명에서 추출 시도
            let fileNameDatePattern = @"(\d{6})_"  // 250103_ 형태
            let dateMatch = Regex.Match(fileName, fileNameDatePattern)
            
            if dateMatch.Success then
                let dateStr = dateMatch.Groups.[1].Value
                try
                    let year = 2000 + int (dateStr.Substring(0, 2))
                    let month = int (dateStr.Substring(2, 2))
                    let day = int (dateStr.Substring(4, 2))
                    Some (System.DateTime(year, month, day))
                with
                | _ -> None
            else
                None
    
    // 마크다운 내용에서 첫 번째 문단을 요약으로 추출
    let extractSummary (markdownContent: string) =
        // YAML 프론트매터 제거
        let contentWithoutFrontMatter = removeYamlFrontMatter markdownContent
        
        // 첫 번째 헤딩 이후 첫 번째 문단 찾기
        let lines = contentWithoutFrontMatter.Split([|'\n'|])
        let mutable summary = ""
        let mutable foundFirstHeading = false
        let mutable foundSummary = false
        
        for line in lines do
            let trimmedLine = (line: string).Trim()
            if not foundSummary then
                if trimmedLine.StartsWith("#") then
                    foundFirstHeading <- true
                elif foundFirstHeading && trimmedLine.Length > 0 && not (trimmedLine.StartsWith("#")) then
                    summary <- trimmedLine
                    foundSummary <- true
                elif not foundFirstHeading && trimmedLine.Length > 0 && not (trimmedLine.StartsWith("#")) then
                    summary <- trimmedLine
                    foundSummary <- true
        
        if summary.Length > 150 then
            Some (summary.Substring(0, 150) + "...")
        elif summary.Length > 0 then
            Some summary
        else
            None

module CanvasParser =
    open System.Text.RegularExpressions
    open System.IO
    
    // JSON에서 문자열 값 추출 (개선된 파서)
    let extractStringValue (json: string) (key: string) =
        let pattern = $@"""{key}""\s*:\s*""((?:[^""\\]|\\.)*)"""
        let match_ = Regex.Match(json, pattern)
        if match_.Success then 
            let value = match_.Groups.[1].Value
            // JSON 이스케이프 문자 복원
            let unescapedValue = 
                value
                    .Replace("\\\"", "\"")
                    .Replace("\\\\", "\\")
                    .Replace("\\n", "\n")
                    .Replace("\\r", "\r")
                    .Replace("\\t", "\t")
            Some unescapedValue
        else None
    
    // JSON에서 정수 값 추출
    let extractIntValue (json: string) (key: string) =
        let pattern = $@"""{key}""\s*:\s*(-?\d+)"
        let match_ = Regex.Match(json, pattern)
        if match_.Success then 
            match System.Int32.TryParse(match_.Groups.[1].Value) with
            | true, value -> Some value
            | false, _ -> None
        else None
    
    // 노드 파싱
    let parseNode (nodeJson: string) =
        let id = extractStringValue nodeJson "id" |> Option.defaultValue ""
        let nodeType = extractStringValue nodeJson "type" |> Option.defaultValue "text"
        let text = extractStringValue nodeJson "text"
        let file = extractStringValue nodeJson "file"
        let x = extractIntValue nodeJson "x" |> Option.defaultValue 0
        let y = extractIntValue nodeJson "y" |> Option.defaultValue 0
        let width = extractIntValue nodeJson "width" |> Option.defaultValue 250
        let height = extractIntValue nodeJson "height" |> Option.defaultValue 60
        
        {
            Id = id
            Type = nodeType
            Text = text
            File = file
            X = x
            Y = y
            Width = width
            Height = height
        }
    
    // 엣지 파싱
    let parseEdge (edgeJson: string) =
        let id = extractStringValue edgeJson "id" |> Option.defaultValue ""
        let fromNode = extractStringValue edgeJson "fromNode" |> Option.defaultValue ""
        let toNode = extractStringValue edgeJson "toNode" |> Option.defaultValue ""
        let fromSide = extractStringValue edgeJson "fromSide"
        let toSide = extractStringValue edgeJson "toSide"
        
        {
            Id = id
            FromNode = fromNode
            ToNode = toNode
            FromSide = fromSide
            ToSide = toSide
        }
    
    // JSON 배열 분할 (개선된 파서)
    let splitJsonArray (jsonArray: string) =
        let mutable level = 0
        let mutable start = 0
        let mutable results = []
        let mutable inString = false
        let mutable escaped = false
        let chars = jsonArray.ToCharArray()
        
        for i = 0 to chars.Length - 1 do
            let char = chars.[i]
            
            if inString then
                if escaped then
                    escaped <- false
                elif char = '\\' then
                    escaped <- true
                elif char = '"' then
                    inString <- false
            else
                match char with
                | '"' -> inString <- true
                | '{' -> level <- level + 1
                | '}' -> 
                    level <- level - 1
                    if level = 0 then
                        let item = jsonArray.Substring(start, i - start + 1).Trim()
                        if item.Length > 0 then
                            results <- item :: results
                        start <- i + 1
                | ',' when level = 0 -> 
                    start <- i + 1
                | _ -> ()
        
        List.rev results
    
    // Canvas 파일 파싱 (개선된 JSON 파서)
    let parseCanvas (filePath: string) =
        let fileName = Path.GetFileNameWithoutExtension(filePath)
        let urlFriendlyName = Url.toUrlFriendly fileName
        let content = File.ReadAllText(filePath)
        
        try
            // System.Text.Json을 사용한 파싱
            let jsonDocument = System.Text.Json.JsonDocument.Parse(content)
            let root = jsonDocument.RootElement
            
            // nodes 배열 파싱
            let nodes = 
                let mutable prop = Unchecked.defaultof<System.Text.Json.JsonElement>
                if root.TryGetProperty("nodes", &prop) then
                    let nodesArray = root.GetProperty("nodes")
                    nodesArray.EnumerateArray()
                    |> Seq.map (fun nodeElement ->
                        let getId () = 
                            let mutable idProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if nodeElement.TryGetProperty("id", &idProp) then
                                nodeElement.GetProperty("id").GetString()
                            else ""
                        let getType () = 
                            let mutable typeProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if nodeElement.TryGetProperty("type", &typeProp) then
                                nodeElement.GetProperty("type").GetString()
                            else "text"
                        let getText () = 
                            let mutable textProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if nodeElement.TryGetProperty("text", &textProp) then
                                Some (nodeElement.GetProperty("text").GetString())
                            else None
                        let getFile () = 
                            let mutable fileProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if nodeElement.TryGetProperty("file", &fileProp) then
                                Some (nodeElement.GetProperty("file").GetString())
                            else None
                        let getInt (prop: string) defaultValue =
                            let mutable intProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if nodeElement.TryGetProperty(prop, &intProp) then
                                nodeElement.GetProperty(prop: string).GetInt32()
                            else defaultValue
                        
                        {
                            Id = getId()
                            Type = getType()
                            Text = getText()
                            File = getFile()
                            X = getInt "x" 0
                            Y = getInt "y" 0
                            Width = getInt "width" 250
                            Height = getInt "height" 60
                        })
                    |> Seq.toList
                else []
            
            // edges 배열 파싱
            let edges = 
                let mutable edgesProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                if root.TryGetProperty("edges", &edgesProp) then
                    let edgesArray = root.GetProperty("edges")
                    edgesArray.EnumerateArray()
                    |> Seq.map (fun edgeElement ->
                        let getId () = 
                            let mutable idProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if edgeElement.TryGetProperty("id", &idProp) then
                                edgeElement.GetProperty("id").GetString()
                            else ""
                        let getFromNode () = 
                            let mutable fromProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if edgeElement.TryGetProperty("fromNode", &fromProp) then
                                edgeElement.GetProperty("fromNode").GetString()
                            else ""
                        let getToNode () = 
                            let mutable toProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if edgeElement.TryGetProperty("toNode", &toProp) then
                                edgeElement.GetProperty("toNode").GetString()
                            else ""
                        let getSide (prop: string) =
                            let mutable sideProp = Unchecked.defaultof<System.Text.Json.JsonElement>
                            if edgeElement.TryGetProperty(prop, &sideProp) then
                                Some (edgeElement.GetProperty(prop: string).GetString())
                            else None
                        
                        {
                            Id = getId()
                            FromNode = getFromNode()
                            ToNode = getToNode()
                            FromSide = getSide "fromSide"
                            ToSide = getSide "toSide"
                        })
                    |> Seq.toList
                else []
            
            {
                Title = fileName
                Url = urlFriendlyName + ".html"
                Nodes = nodes
                Edges = edges
            }
        with
        | ex ->
            printfn $"Error parsing canvas file {fileName}: {ex.Message}"
            {
                Title = fileName
                Url = urlFriendlyName + ".html"
                Nodes = []
                Edges = []
            }
