#include <bits/stdc++.h>
using namespace std;



void binarysearch(int a[],int low,int high)
{ 
	  int mid;
	  if (low > high)
	  {
		  printf("Error");
	  }
	  mid = (low + high)/2;
	  if(mid == a[mid])
	  { 
	
		printf(" %d ", mid);
	      	
	  }
	  if(mid < a[mid])
	  { 
		high = mid - 1;
	        binarysearch(a,low,high);
	  }
	  if(mid > a[mid])
	  { 
		low = mid + 1;
       	        binarysearch(a,low,high);
	  }
}	
	

int main()
{
	// freopen("in.txt","r",stdin);
	// freopen("out.txt","w",stdout);
	int a[1000100],i,mid,t,k,n;
	// printf("enter the no of test cases\t");
	cin>>t;
	
	// a=(int*)malloc(sizeof(int)*n);
	for(k=0;k<t;k++)
	{
		cin>>n;
		int f=0;
		for(i=0;i<n;i++)
		{
			cin>>a[i];
		}
		for(int i=0;i<n;i++)
		{
			if(a[i]==i)
			{
				f=1;
				cout<<i<<"\n";
				break;
			}
		}       
		if(!f)
		{
			cout<<"-1\n";
		} 
	}
while(1);
	return 0;
}
