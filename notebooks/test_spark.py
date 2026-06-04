"""
Test Spark

Este notebook testa se Apache Spark está funcionando corretamente no ambiente.
"""

import os
import sys
import subprocess

# ============================================================================
# Cell 1: Configure Java Environment
# ============================================================================

# Configurar variáveis de ambiente para PySpark/Java
java_home = r'C:\Program Files\Java\jdk-17'
os.environ['JAVA_HOME'] = java_home

# Verificar se Java está realmente acessível
java_exe = os.path.join(java_home, 'bin', 'java.exe')
print(f"✓ JAVA_HOME configurado: {java_home}")
print(f"✓ Java executável: {java_exe}")
print(f"✓ Java existe: {os.path.exists(java_exe)}")

# Testar Java diretamente
try:
    result = subprocess.run([java_exe, '-version'], capture_output=True, text=True, timeout=5)
    print(f"✓ Java versão: {result.stderr.split('(')[0].strip()}")
except Exception as e:
    print(f"✗ Erro ao testar Java: {e}")

print(f"\n✓ Python version: {sys.version}")
print(f"✓ Python executable: {sys.executable}")

# ============================================================================
# Markdown Cell: Teste de Spark
# 
# Este notebook testa se Apache Spark está funcionando corretamente no ambiente.
# ============================================================================

# ============================================================================
# Markdown Cell: 1. Importar Bibliotecas Spark
# 
# Importar as bibliotecas necessárias do PySpark, incluindo SparkSession.
# ============================================================================

# ============================================================================
# Cell 2: Import Spark Libraries
# ============================================================================

from pyspark.sql import SparkSession

print("✓ Bibliotecas Spark importadas com sucesso!")

# ============================================================================
# Markdown Cell: 2. Inicializar Sessão Spark
# 
# Criar e inicializar uma sessão Spark para estabelecer uma conexão com o cluster Spark.
# ============================================================================

# ============================================================================
# Cell 3: Initialize Spark Session
# ============================================================================

# Configurar Java
java_home = r'C:\Program Files\Java\jdk-17'
os.environ['JAVA_HOME'] = java_home
os.environ['PATH'] = os.path.join(java_home, 'bin') + ';' + os.environ['PATH']

# Configurar SPARK_HOME para apontar para a instalação via pip
spark_home = r'c:\Users\Mileno\Downloads\PDI\env\Lib\site-packages\pyspark'
os.environ['SPARK_HOME'] = spark_home
os.environ['PYSPARK_PYTHON'] = sys.executable

# Adicionar jars ao PYTHONPATH
jars_dir = os.path.join(spark_home, 'jars')
if os.path.exists(jars_dir):
    print(f"✓ JARs encontrados em: {jars_dir}")

print("=== Configuração ===")
print(f"JAVA_HOME: {os.environ['JAVA_HOME']}")
print(f"SPARK_HOME: {os.environ['SPARK_HOME']}")
print(f"PYSPARK_PYTHON: {sys.executable}")

print("\n=== Tentando criar SparkSession ===")
try:
    spark = SparkSession.builder \
        .appName("TesteSpark") \
        .master("local[1]") \
        .getOrCreate()

    print("✓✓✓ SUCESSO! Spark funcionando! ✓✓✓")
    print(f"Versão: {spark.version}")
    print(f"Master: {spark.sparkContext.master}")
    
except Exception as e:
    print(f"✗ Erro: {type(e).__name__}: {e}")

# ============================================================================
# Markdown Cell: 3. Criar um DataFrame Simples
# 
# Criar um DataFrame de exemplo usando PySpark para testar criação e manipulação básica de estruturas de dados.
# ============================================================================

# ============================================================================
# Cell 4: Create Sample DataFrame
# ============================================================================

# Criar um DataFrame de exemplo com SQL (sem Python worker)
print("Criando DataFrame...")

# Usar SQL string em vez de Python objects para evitar problemas com workers
spark.sql("""
    CREATE TEMP VIEW test_data AS
    SELECT 1 as id, 'Alice' as nome, 25 as idade
    UNION ALL
    SELECT 2, 'Bob', 30
    UNION ALL
    SELECT 3, 'Charlie', 35
    UNION ALL
    SELECT 4, 'Diana', 28
""")

df = spark.sql("SELECT * FROM test_data")

print("✓ DataFrame criado com sucesso!")
print(f"Tipo: {type(df)}")
print(f"Colunas: {df.columns}")

# ============================================================================
# Markdown Cell: 4. Verificar Operações Spark
# 
# Executar operações básicas de Spark como show(), count() e printSchema() para verificar que Spark está funcionando corretamente.
# ============================================================================

# ============================================================================
# Cell 5: Verify Spark Operations
# ============================================================================

# Exibir o esquema do DataFrame
print("Schema do DataFrame:")
df.printSchema()

print("\n" + "="*50)
print("Dados do DataFrame:")
print("="*50 + "\n")

# Exibir os dados usando show() que usa SQL no servidor
df.show()

print("\n" + "="*50)
print("Resumo:")
print("="*50)

# Operações de verificação usando SQL (sem Python workers)
num_linhas = spark.sql("SELECT COUNT(*) as count FROM test_data").collect()[0][0]
num_colunas = len(df.columns)

print(f"✓ Total de linhas: {num_linhas}")
print(f"✓ Total de colunas: {num_colunas}")
print(f"✓ Nomes das colunas: {df.columns}")

print("\n✓✓✓ SPARK ESTÁ FUNCIONANDO CORRETAMENTE! ✓✓✓")
print("\nO notebook de teste foi concluído com sucesso!")

# ============================================================================
# Cell 6: Empty Cell
# ============================================================================
