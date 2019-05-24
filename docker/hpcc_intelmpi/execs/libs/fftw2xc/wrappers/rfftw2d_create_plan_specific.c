/*******************************************************************************
* Copyright 2010-2018 Intel Corporation.
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
 * rfftw2d_create_plan_specific - FFTW2 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

#include "fftw2_mkl.h"

rfftwnd_plan
rfftw2d_create_plan_specific(int nx, int ny, fftw_direction dir, int flags,
        fftw_real *in, int istride, fftw_real *out, int ostride)
{
    int n[2];
    n[0] = nx;
    n[1] = ny;
    return rfftwnd_create_plan_specific(2, n, dir, flags, in, istride, out,
            ostride);
}
