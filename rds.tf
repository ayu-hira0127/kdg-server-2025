# # RDSパスワード用の変数
# variable "rds_password" {
#   description = "RDS で使うパスワード"
#   type        = string
#   default     = "vantan1234"
# }

# # デフォルトVPCの情報を取得
# data "aws_vpc" "main" {
#   default = true
# }

# # RDS用のサブネットグループを作成
# resource "aws_db_subnet_group" "postgresql" {
#   name       = "postgresql-subnet-group"
#   subnet_ids = data.aws_subnets.default.ids

#   tags = {
#     Name = "postgresql-subnet-group"
#   }
# }

# # デフォルトVPCのサブネット情報を取得
# data "aws_subnets" "default" {
#   filter {
#     name   = "vpc-id"
#     values = [data.aws_vpc.main.id]
#   }
# }

# # RDS用のセキュリティグループを作成
# resource "aws_security_group" "postgresql" {
#   name        = "postgresql-sg"
#   description = "Security group for PostgreSQL RDS"
#   vpc_id      = data.aws_vpc.main.id

#   # PostgreSQLのデフォルトポート（5432）を許可
#   ingress {
#     from_port   = 5432
#     to_port     = 5432
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   # すべてのアウトバウンドトラフィックを許可
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   tags = {
#     Name = "postgresql-sg"
#   }
# }

# # PostgreSQL RDSインスタンスを作成
# resource "aws_db_instance" "postgresql" {
#   # データベース設定
#   identifier           = "postgresql-db"
#   engine               = "postgres"
#   engine_version       = "17.4"
#   parameter_group_name = "default.postgres17"  # デフォルトのパラメータグループを使用
#   instance_class       = "db.t4g.micro"
  
#   # ストレージ設定（無料枠に収める）
#   allocated_storage = 20
#   storage_type      = "gp2"  # gp3からgp2に変更（無料枠対応）
#   storage_encrypted = false  # 暗号化無効（無料枠対応）
  
#   # データベース認証情報
#   db_name  = "myapp"
#   username = "postgres"
#   password = var.rds_password  # 変数化
#   port     = 5432
  
#   # ネットワーク設定
#   db_subnet_group_name   = aws_db_subnet_group.postgresql.name
#   vpc_security_group_ids = [aws_security_group.postgresql.id]
#   publicly_accessible    = true  # パブリックアクセスを有効化
  
#   # 可用性関連の設定（無料枠で収めるため）
#   multi_az = false  # マルチAZ無効
  
#   # バックアップとスナップショット設定（すべて無効）
#   backup_retention_period   = 0      # バックアップ無効
#   skip_final_snapshot       = true   # 削除時のスナップショット作成をスキップ
#   delete_automated_backups  = true   # 自動バックアップを削除
#   copy_tags_to_snapshot     = false  # タグをスナップショットにコピーしない
  
#   # モニタリング設定（無料枠対応）
#   monitoring_interval          = 0     # 拡張モニタリング無効
#   performance_insights_enabled = false # Performance Insights無効
  
#   # メンテナンス設定
#   maintenance_window = "sun:03:00-sun:04:00"
  
#   # セキュリティ関連
#   ca_cert_identifier = "rds-ca-rsa4096-g1"
  
#   # ログ設定
#   enabled_cloudwatch_logs_exports = ["postgresql"]
  
#   # 削除保護
#   deletion_protection = false  # 開発環境なので無効
  
#   tags = {
#     Name        = "postgresql-db"
#     Environment = "development"
#   }
# }

# # RDS接続情報を出力
# output "rds_endpoint" {
#   description = "RDS のエンドポイント"
#   value       = aws_db_instance.postgresql.address
#   sensitive   = false
# }

# output "rds_port" {
#   description = "RDS instance port"
#   value       = aws_db_instance.postgresql.port
# }

# output "rds_database_name" {
#   description = "RDS database name"
#   value       = aws_db_instance.postgresql.db_name
# } 