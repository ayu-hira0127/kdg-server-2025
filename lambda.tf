# CI/CD側でlambdaのソースコードを格納するための箱
# resource "aws_s3_bucket" "lambda_artifacts" {
#   # AWS S3 で一意である(重複がない)必要がある
#   # 例) kdg-aws-2025-ここに自分のgithubのユーザー名-lambda-artifacts
#   bucket = "aws-2025-hiramoto-lambda-artifacts"
#   tags = {
#     # bucket に指定した内容と同じものを書く
#     Name = "aws-2025-hiramoto-lambda-artifacts"
#   }
# }

# lambda 実行時に必要な権限をまとめる role を定義する
resource "aws_iam_role" "lambda" {
  name = "iam_for_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}

# CloudWatch Logs への書き込み権限を 定義した role に対して付与する
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# GetAccountSettings も実行時に必要な権限なので付与する
resource "aws_iam_role_policy" "get_account_settings" {
  name = "GetAccountSettingsPermission"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "lambda:GetAccountSettings"
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

# 初回のみ利用する Lambda のファイルを生成
# data "archive_file" "initial_lambda_package" {
#   type        = "zip"
#   output_path = "${path.module}/.temp_files/lambda.zip"
#   source {
#     # 実際に動作するPythonコードに修正
#     content = <<EOF
# import json

# def lambda_handler(event, context):
#     return {
#         'statusCode': 200,
#         'headers': {
#             'Content-Type': 'application/json'
#         },
#         'body': json.dumps({
#             'message': 'Hello from Lambda!',
#             'function_name': context.function_name,
#             'request_id': context.aws_request_id,
#             'event': event
#         })
#     }
# EOF
#     filename = "lambda_function.py"
#   }
# }

# (初回のみ)LambdaのファイルをS3にアップロード
# resource "aws_s3_object" "lambda_file" {
#   bucket = aws_s3_bucket.lambda_artifacts.id
#   key    = "initial.zip"
#   source = data.archive_file.initial_lambda_package.output_path
# }

# Lambda関数を生成
# resource "aws_lambda_function" "first_function" {
#   function_name = "first-function"
#   role          = aws_iam_role.lambda.arn
#   handler       = "lambda_function.lambda_handler"
#   runtime       = "python3.12"
#   timeout       = 120
#   publish       = true
#   s3_bucket     = aws_s3_bucket.lambda_artifacts.id
#   s3_key        = aws_s3_object.lambda_file.key
#   depends_on = [aws_s3_object.lambda_file]
# }

# 外部からリクエストを飛ばすためのエンドポイント
# resource "aws_lambda_function_url" "first_function" {
#   function_name      = aws_lambda_function.first_function.function_name
#   authorization_type = "NONE"
# }

# 出力値を追加
# output "lambda_function_url" {
#   value = aws_lambda_function_url.first_function.function_url
# }

# output "lambda_function_name" {
#   value = aws_lambda_function.first_function.function_name
# }

# output "s3_bucket_name" {
#   value = aws_s3_bucket.lambda_artifacts.id
# }