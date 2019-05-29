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
 * rfftwnd_one_complex_to_real - FFTW2 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

#include "fftw2_mkl.h"

void
rfftwnd_one_complex_to_real(rfftwnd_plan plan, fftw_complex *in,
                            fftw_real *out)
{
    rfftwnd_complex_to_real(plan, 1, in, 1, 0, out, 1, 0);
}
