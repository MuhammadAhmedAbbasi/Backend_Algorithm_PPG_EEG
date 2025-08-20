$tips = "Tips: to use this script, you need to install protoc and make sure protoc is in the environment variable."
Write-Host $tips

$oldLocation = Get-Location
$baseDir = "grpc_modules"
Set-Location -Path $baseDir

$outDir = "generated"
# 确保grpc文件夹存在，如果不存在，则创建

if (-Not (Test-Path -Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir
}

# 获取protos文件夹中的所有.proto文件
$protoDir = "protos"
$protoFiles = Get-ChildItem -Path $protoDir -Filter "*.proto"

# 为每个.proto文件生成Python代码
foreach ($file in $protoFiles) {
    & python -m grpc_tools.protoc --proto_path=$protoDir  --python_out=$outDir  --grpc_python_out=$outDir $file.Name
    & protoc --python_out=$outDir --proto_path=$protoDir --mypy_out=$outDir $file.Name
}

Set-Location -Path $oldLocation

Write-Host "Generated Python code for gRPC services in $baseDir\$outDir"