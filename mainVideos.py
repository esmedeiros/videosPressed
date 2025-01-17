from flask import Flask, jsonify
import boto3

# Configurações
app = Flask(__name__)
BUCKET_NAME = "chunkvideopressed"  # Substitua pelo nome do seu bucket

# Inicializa cliente S3
s3_client = boto3.client('s3')


@app.route('/videos', methods=['GET'])
def list_videos():
    """
    Lista os vídeos disponíveis no bucket S3.

    Returns:
        JSON: Lista de arquivos com seus caminhos no S3.
    """
    try:
        # Lista os objetos no bucket
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='videos_pressed/')
        files = []

        # Adiciona os arquivos na lista
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    "file_name": obj['Key'].split('/')[-1],
                    "s3_path": obj['Key'],
                    "size": obj['Size'],
                    "last_modified": obj['LastModified'].isoformat()
                })

        return jsonify({
            "status": "success",
            "videos": files
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)