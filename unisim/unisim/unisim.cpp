#include <iostream>
#include <WinSock2.h>
#include <stdlib.h>
#include <assert.h>

#include "universe.hpp"
#include "MIMOServer.hpp"

int32_t compare(const void* aV, const void* bV)
{
	uint64_t a = *(uint64_t*)aV;
	uint64_t b = *(uint64_t*)bV;
	return ((a < b) ? -1 : ((a == b) ? 0 : 1));
}

void dc(int32_t c)
{
	fprintf(stderr, "DC %d\n", c);
	char buf[1024];
	int32_t ngot = recv(c, buf, 1023, 0);
	if (ngot == SOCKET_ERROR)
	{
		ngot = WSAGetLastError();
		fprintf(stderr, "Couldn't read from socket %d (%d)\n", c, ngot);
		return;
	}

	buf[ngot] = 0;
	fprintf(stderr, "%s", buf);
}

void hc(int32_t c)
{
	fprintf(stderr, "HC %d\n", c);
}

void main(int32_t argc, char** argv)
{
	try
	{
		Universe u(0.001, 0.001, 0.01, 5505, 2);
		u.start_net();
		u.start_sim();
		char input[128];
		std::cin >> input;
		u.stop_net();
		u.stop_sim();
	}
	catch (char* e)
	{
		fprintf(stderr, "Caught error: %s\n", e);
	}
}
