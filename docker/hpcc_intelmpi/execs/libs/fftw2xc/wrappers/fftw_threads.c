/*******************************************************************************
* Copyright 2006-2018 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

/*
 *
 * fftw_threads - FFTW2 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

#include "fftw2_mkl.h"

void
fftw_threads(int nthreads, fftw_plan plan, int howmany, fftw_complex *in,
             int istride, int idist, fftw_complex *out, int ostride, int odist)
{
    fftwnd_threads(nthreads, (fftwnd_plan)plan,
            howmany, in, istride, idist, out, ostride, odist);
}
