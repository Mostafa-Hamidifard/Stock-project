import asyncio
import aiohttp
import os


async def _download_csv(url, id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            return [id, content]


async def _write_to_file(path, name, format, content):
    if(os.path.exists(path) == 0):
        os.makedirs(path)
    filename = os.path.join(path, f"{name}.{format}")
    with open(filename, "wb") as pep_file:
        pep_file.write(content)


def _generateLinks(id_path, sample_url):
    """it generates original pathes for downloading
    returns: URL pathes as a {id:url} dictionary """
    url_list = []
    IDs = []
    with open(id_path, mode="r") as f:
        IDs = [line.strip('\n') for line in f]

        url_list = [
            sample_url+id for id in IDs]
    return url_list, IDs


async def _main(url_list, save_path, format):
    tasks = [asyncio.create_task(_download_csv(url, id))
             for url, id in url_list.items()]
    contentsAndId = [await task for task in tasks]
    for package in contentsAndId:
        await _write_to_file(save_path, package[0], format, package[1])


def start_downloading_data_and_store(IDs_path, store_path=os.getcwd(), sample_url="http://dev.tsetmc.com/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i=", saving_format="csv"):
    """USE this function to download data with IDs written in file in <IDs_path> and store them in <store_path> folder
    input params: ID_path(required,it has to be absolute path) ,store_path(default=os.path.getcwd()), sample_url(optional),, saving_format(default=csv)
    returns: nothing"""
    url_list, IDs = _generateLinks(IDs_path, sample_url)
    asyncio.run(_main(dict(zip(url_list, IDs)),
                store_path, saving_format))


if __name__ == '__main__':
    print("receive data started")
    start_downloading_data_and_store(
        "Mostafa//stocks.txt", "E:\\ap_final\\Mostafa")
