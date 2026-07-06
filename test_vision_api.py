#!/usr/bin/env python3
"""
Teste de integração com Google Cloud Vision API para E-Lixo.
Execute este script para testar se a API está funcionando corretamente.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import classify_with_vision_api, CATEGORY_EXPLANATIONS

def test_vision_api():
    """Teste básico da Vision API"""
    
    print("=" * 70)
    print("🤖 Teste de Google Cloud Vision API - E-Lixo")
    print("=" * 70)
    
    # Verificar se credenciais estão configuradas
    creds_env = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_env:
        # fallback: try to find a JSON key file in the tests folder and project root
        search_dirs = [os.path.dirname(os.path.abspath(__file__)), os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))]
        for search_dir in search_dirs:
            for filename in os.listdir(search_dir):
                if filename.lower().endswith('.json'):
                    candidate = os.path.join(search_dir, filename)
                    try:
                        with open(candidate, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if 'private_key' in content and 'client_email' in content:
                            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = candidate
                            creds_env = candidate
                            break
                    except Exception:
                        continue
            if creds_env:
                break

    if not creds_env:
        print('  $env:GOOGLE_APPLICATION_CREDENTIALS="C:\\caminho\\para\\arquivo.json"')
        print("\nVeja SETUP_GOOGLE_VISION.md para instruções completas.")
        return False
    
    print(f"\n✅ Credenciais encontradas: {creds_env}")
    
    # Procurar por imagens de teste
    test_images = []
    if os.path.exists('test_upload.jpg'):
        test_images.append('test_upload.jpg')
    
    for filename in os.listdir('uploads'):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            test_images.append(os.path.join('uploads', filename))
            if len(test_images) >= 3:
                break
    
    if not test_images:
        print("\n⚠️  Nenhuma imagem de teste encontrada.")
        print("   Coloque imagens em: uploads/ ou test_upload.jpg")
        print("\n💡 Sugestão: Tire uma foto de um eletrônico e coloque em 'uploads/'")
        return False
    
    print(f"\n📷 Encontradas {len(test_images)} imagens para teste:")
    
    success_count = 0
    for img_path in test_images:
        print(f"\n  → Testando: {img_path}")
        
        try:
            result = classify_with_vision_api(img_path)
            
            if isinstance(result, dict) and result.get('error'):
                print(f"    ⚠️  Erro na classificação: {result.get('error')} - {result.get('message')}")
            elif result:
                # ensure keys exist
                label = result.get('label')
                category = result.get('category')
                confidence = result.get('confidence')
                if label is None or category is None or confidence is None:
                    print(f"    ⚠️  Resposta inesperada da IA: {result}")
                else:
                    print(f"    ✅ Sucesso!")
                    print(f"       Rótulo detectado: {label}")
                    print(f"       Categoria: {category}")
                    print(f"       Confiança: {confidence * 100:.1f}%")
                    if 'detected_objects' in result:
                        print(f"       Objetos: {', '.join(result['detected_objects'][:3])}")
                    success_count += 1
            else:
                print(f"    ⚠️  Nenhuma detecção")
                
        except Exception as e:
            print(f"    ❌ Erro: {str(e)}")
    
    print("\n" + "=" * 70)
    print(f"📊 Resultado: {success_count}/{len(test_images)} imagens processadas com sucesso")
    
    if success_count > 0:
        print("\n✨ Vision API está funcionando!")
        print("   Agora você pode fazer upload de imagens no site e elas serão")
        print("   automaticamente classificadas e categorizadas! 🎉")
    else:
        print("\n❌ Verifique as credenciais do Google Cloud")
    
    print("=" * 70)
    return success_count > 0


if __name__ == '__main__':
    test_vision_api()
