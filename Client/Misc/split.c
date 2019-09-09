#include <stdio.h>  
#include <stddef.h>  
#include <stdlib.h>  
#include <wchar.h>  
#include <Windows.h>

#define BLOCK_SIZE 65536

int widechar_main( int argc, wchar_t *argv[ ] ) {

	if (argc!=3) {
		fprintf(stderr,"Dame 2 argumentos");
		return 255;
	}

	FILE *f = _wfopen(argv[1],L"rb");
	if (!f) {
		wprintf(L"No se puede leer archivo fuente: %s\n",argv[1]);
	}

	size_t chunksize=_wtoi(argv[2])*1024*1024;
	int chunk=0;
	int eof=0;

	while(!eof) {

		wchar_t buf[1024];
		swprintf(buf,L"%s.chunk%i",argv[1],chunk);
		FILE *g = _wfopen(buf,L"wb");
		if (!g) {
			wprintf(L"No se puede leer archivo destino: %s\n",argv[2]);
		}	

		size_t todo=chunksize;

		while(todo) {

				unsigned char block[BLOCK_SIZE];

				size_t to_read = todo < BLOCK_SIZE ? todo : BLOCK_SIZE;

				size_t gotbytes = fread(block,1,to_read,f);

				if (gotbytes) {
					fwrite(block,gotbytes,1,g);
				}

				if (gotbytes < to_read) {
					eof=1;
					break;
				}

				todo-=to_read;

		}

		fclose(g);

		if (todo<chunksize) {
				wprintf(L"%s\n",buf);
		}
		chunk++;
	}

	fclose(f);

	return 0;

}

int main(int _argc, char** _argv) {
	// _argc and _argv are ignored
	// we are going to use the WideChar version of them instead

	LPWSTR *wc_argv;
	int    argc;
	int    result;

	wc_argv = CommandLineToArgvW(GetCommandLineW(), &argc);

	if( NULL == wc_argv )	{
		wprintf(L"CommandLineToArgvW failed\n");
		return 0;
	}

	result = widechar_main(argc, wc_argv);

	LocalFree(wc_argv);
	return result;
}