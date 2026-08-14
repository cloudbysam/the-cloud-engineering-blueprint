variable "username" {
  description = "The username to use for the database server"
  type        = string
  sensitive   = true
}

variable "password" {
  description = "The password to use for the database server"
  type        = number
  sensitive   = true
}