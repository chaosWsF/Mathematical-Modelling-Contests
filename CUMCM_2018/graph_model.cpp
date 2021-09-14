#include <cstdio>
using namespace std;
const int _inf = 0x7fffffff;
const int inf = _inf/3;	//
const int maxn = 105;  
int graph[maxn][maxn], pre[maxn][maxn], dis[maxn][maxn];
int cnt, path[maxn], sum;
int n, m;  
void init()  
{ 
    for(int i = 1; i <= n; ++i) 
    { 
    	for(int j = 1; j <= n; ++j)
    	{
    		pre[i][j] = i;
    		graph[i][j] = dis[i][j] = inf;
    	}
    	graph[i][i] = dis[i][i] = 0;
    } 
}
void Folyd()  
{  
    int mins = inf;
    for(int k = 1; k <= n; ++k)
    {
    	for(int i = 1; i < k; ++i)
    	for(int j = i+1; j < k; ++j)
    	{
    		//
    		int tmp = dis[i][j] + graph[k][i] + graph[j][k];	
    		//
    		if(mins > tmp)
    		{
    			mins = tmp;
    			cnt = 0; sum = 1;
    			int t = i;
    			while(t != j)
    			{
					path[cnt++] = t;
					t = pre[j][t];
				}
				path[cnt++] = j;
				path[cnt++] = k;
    		}
    		else if(tmp == mins) ++sum;	//
    	}
    	for(int i = 1; i <= n; ++i)
    	for(int j = 1; j <= n; ++j)
    	{
    		if(dis[i][j] > dis[i][k]+dis[k][j])
    		{
    			dis[i][j] = dis[i][k]+dis[k][j];
    			pre[i][j] = pre[k][j];
    		}
    	}
    }
    if(mins == inf) puts("No solution.");
    else
    {
    	for(int i = cnt-1; i > 0; --i) printf("%d ", path[i]);
    	printf("%d\n", path[0]);
    }
}
int main()  
{  
    int u, v, w;  
    while(~scanf("%d %d", &n, &m))
    {
	    init();  
	    for(int i = 1; i <= m; ++i)  
	    {  
	        scanf("%d %d %d", &u, &v, &w); 
	        if(w < graph[u][v])
	        {
		        graph[u][v] = graph[v][u] = w;
		        dis[u][v] = dis[v][u] = w; 
		    }
	    }  
	    Folyd(); 
	}
    return 0;  
}
