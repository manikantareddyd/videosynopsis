//////////////////////////////////////////////////////////////////////////////
// Example illustrating the use of GCoptimization.cpp
//
/////////////////////////////////////////////////////////////////////////////
//
//  Optimization problem:
//  is a set of sites (pixels) of width 10 and hight 5. Thus number of pixels is 50
//  grid neighborhood: each pixel has its left, right, up, and bottom pixels as neighbors
//  7 labels
//  Data costs: D(pixel,label) = 0 if pixel < 25 and label = 0
//            : D(pixel,label) = 10 if pixel < 25 and label is not  0
//            : D(pixel,label) = 0 if pixel >= 25 and label = 5
//            : D(pixel,label) = 10 if pixel >= 25 and label is not  5
// Smoothness costs: V(p1,p2,l1,l2) = min( (l1-l2)*(l1-l2) , 4 )
// Below in the main program, we illustrate different ways of setting data and smoothness costs
// that our interface allow and solve this optimizaiton problem

// For most of the examples, we use no spatially varying pixel dependent terms.
// For some examples, to demonstrate spatially varying terms we use
// V(p1,p2,l1,l2) = w_{p1,p2}*[min((l1-l2)*(l1-l2),4)], with
// w_{p1,p2} = p1+p2 if |p1-p2| == 1 and w_{p1,p2} = p1*p2 if |p1-p2| is not 1

// g++ -shared -c -fPIC example.cpp graph.cpp GCoptimization.cpp LinkedBlockList.cpp maxflow.cpp
// g++ -shared -Wl,-soname,library.so -o library.so example.o
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include "GCoptimization.h"

// namespace std;


struct ForDataFn{
	int numLab;
	int *data;
};


float smoothFn(int p1, int p2, int l1, int l2)
{
	if ( (l1-l2)*(l1-l2) <= 4 ) return((l1-l2)*(l1-l2));
	else return(4);
}

float dataFn(int p, int l, void *data)
{
	ForDataFn *myData = (ForDataFn *) data;
	int numLab = myData->numLab;

	return( myData->data[p*numLab+l] );
}

int GridGraph_DfnSfn(int width,int height,int num_pixels,int num_labels)
{

	int *result = new int[num_pixels];   // stores result of optimization

	// first set up the array for data costs
	int *data = new int[num_pixels*num_labels];
	for ( int i = 0; i < num_pixels; i++ )
		for (int l = 0; l < num_labels; l++ )
			if (i < 25 ){
				if(  l == 0 ) data[i*num_labels+l] = 0;
				else data[i*num_labels+l] = 10;
			}
			else {
				if(  l == 5 ) data[i*num_labels+l] = 0;
				else data[i*num_labels+l] = 10;
			}


	try{
		GCoptimizationGridGraph *gc = new GCoptimizationGridGraph(width,height,num_labels);

		// set up the needed data to pass to function for the data costs
		ForDataFn toFn;
		toFn.data = data;
		toFn.numLab = num_labels;

		gc->setDataCost(&dataFn,&toFn);

		// smoothness comes from function pointer
		gc->setSmoothCost(&smoothFn);

		printf("\nBefore optimization energy is %d",(int)gc->compute_energy());
		gc->expansion(2);// run expansion for 2 iterations. For swap use gc->swap(num_iterations);
		printf("\nAfter optimization energy is %d\n",(int)gc->compute_energy());

		for ( int  i = 0; i < num_pixels; i++ )
			result[i] = gc->whatLabel(i);

		return (int)gc->compute_energy();
		delete gc;
		delete [] result;
		delete [] data;

	}
	catch (GCException e){
		e.Report();
	}

}

extern "C" void something(long * indata, int l,long * outdata)
{
	int width = 10;
	int height = 5;
	int num_pixels = width*height;
	int num_labels = 7;


	int e = GridGraph_DfnSfn(width,height,num_pixels,num_labels);
	for(int i=0;i<l;i++)
	{
		for(int j=0;j<l;j++)
		{
			for(int k=0;k<3;k++)
			{

				outdata[i*15+j*3+k] = i*15 + j*3 + k;

			}
		}
	}
}

int main(int argc, char **argv)
{
	return 0;
}
