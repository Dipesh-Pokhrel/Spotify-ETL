resource "aws_lambda_function" "spotify_data" {
  filename = "../payload.zip"
  function_name = "spotify_data"
  handler = "avg_album_length_playlist.lambda_function"
  role = "${aws_iam_role.lambda_execution_role.arn}"
  runtime = "python3.9"
  timeout = "300"


  environment {
    variables= {
      SPOTIFY_CLIENT_ID = var.TF_VAR_SPOTIPY_CLIENT_ID,
      SPOTIPY_CLIENT_SECRET = var.TF_VAR_SPOTIPY_CLIENT_SECRET
    }
  }
}