from app.googlesearch import search


class GoogleService(object):
    __instance = None
    
    @staticmethod
    def get_google_index(keyword: str, url: str) -> int:
        try:
            print(keyword, url)
            results = search(keyword, safe=None, num_results=50, timeout=10)
            print(results)
            for index, result in enumerate(results):
                new_result = result.replace("https://", "").replace("http://", "").rstrip('/')
                new_url = url.replace("https://", "").replace("http://", "").rstrip('/')
                if new_url in new_result:
                    return index
            return -1
        except Exception as e:
            return 0
