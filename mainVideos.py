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
    Lista os vídeos disponíveis no bucket S3 e gera URLs pré-assinadas para download.

    Returns:
        JSON: Lista de arquivos com seus caminhos no S3 e URLs pré-assinadas.
    """
    try:
        # Lista os objetos no bucket
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='videos_pressed/')
        files = []

        # Adiciona os arquivos na lista
        if 'Contents' in response:
            for obj in response['Contents']:
                # Gera a URL pré-assinada
                download_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': obj['Key']},
                    ExpiresIn=3600  # URL válida por 1 hora
                )
                files.append({
                    "file_name": obj['Key'].split('/')[-1],
                    "s3_path": obj['Key'],
                    "size": obj['Size'],
                    "last_modified": obj['LastModified'].isoformat(),
                    "download_url": download_url
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
    app.run(debug=True, host='0.0.0.0')