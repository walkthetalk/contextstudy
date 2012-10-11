#include <iostream>
using namespace std;

class CBase {
public:
	CBase()
	{
		cout << "1";
	}

	virtual ~CBase()
	{
		cout << "2";
	}

	virtual void print()
	{
		cout << "3";
	}
};

class CMember {
public:
	CMember()
	{
		cout << "4";
	}

	virtual ~CMember()
	{
		cout << "5";
	}
};

class CChild : public CBase {
public:
	CChild() : CBase()
	{
		cout << "6";
	}

	virtual ~CChild()
	{
		cout << "7";
	}

	virtual void print()
	{
		cout << "8";
	}
private:
	CMember m_mem;
};

int main(int argc, char * const argv[])
{
	CChild inst;

	inst.print();

	return 0;
}
