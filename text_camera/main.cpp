#include "main.h"


int main(int argc, char** argv)
{
    cv::VideoCapture cap;
    // open the default camera, use something different from 0 otherwise;
    // Check VideoCapture documentation.
    if(!cap.open(0))
        return 0;
    cv::Mat frame;
    for(;;) {

        cap.read(frame);
        if (frame.empty())
            break;

        imshow("Source", frame);

        if (cv::waitKey(1) == 27) // stop capturing by pressing ESC
            break;
    }

    std::string outText = read_text(frame);
    std::cout << outText;
    return 0;
}

std::string read_text(cv::Mat frame)
{
    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    api->Init(NULL,"eng",tesseract::OEM_LSTM_ONLY);
    api->SetPageSegMode(tesseract::PSM_AUTO);
    api->SetImage(frame.data, frame.cols, frame.rows, 3, frame.step);
    std::string outText = std::string(api->GetUTF8Text());
    api->End();
    api->ClearPersistentCache();

    return outText;
}