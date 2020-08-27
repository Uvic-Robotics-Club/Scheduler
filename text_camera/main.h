#pragma once
// This is called "guarding" the header file, and should be present in every .h file.
// It prevents duplicate imports and all of the strange issues that can be the result.


#ifndef _main_h
#define _main_h

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "tesseract/baseapi.h"
#include <iostream>

std::string read_text(cv::Mat frame);

#endif
