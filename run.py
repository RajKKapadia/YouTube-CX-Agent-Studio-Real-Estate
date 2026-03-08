if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", port=8080, reload=True)