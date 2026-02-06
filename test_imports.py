try:
    print("1. Probando langchain_community...", end=" ")
    from langchain_community.document_loaders import PyPDFLoader
    print("✅ OK")

    print("2. Probando langchain core...", end=" ")
    from langchain.chains import RetrievalQA
    print("✅ OK")

    print("3. Probando Groq...", end=" ")
    from langchain_groq import ChatGroq
    print("✅ OK")

    print("\n🎉 TODO INSTALADO CORRECTAMENTE.")
except ImportError as e:
    print(f"\n❌ ERROR CRÍTICO: {e}")
    print("Por favor, comparte este error.")