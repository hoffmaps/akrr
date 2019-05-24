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
 * fftw_die - FFTW2 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

#include "fftw2_mkl.h"

void (*fftw_die_hook)(const char *error_string);

/* FFTW2 documentation doesn't cover this function. */
void
fftw_die(const char *s)
{
    if (fftw_die_hook) fftw_die_hook(s);
    fprintf(stderr,"fftw_die: %s\n",s);
    exit(1);
}
