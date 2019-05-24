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
 * rfftwnd_create_plan - FFTW2 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

#include "fftw2_mkl.h"

rfftwnd_plan
rfftwnd_create_plan(int rank, const int *n, fftw_direction dir, int flags)
{
    return rfftwnd_create_plan_specific(rank, n, dir, flags, NULL, 1, NULL, 1);
}