
from huobi.impl.utils import *
from huobi.model.constant import *
from huobi.impl.restapirequestimpl import RestApiRequestImpl
from huobi.impl.utils.timeservice import convert_cst_in_millisecond_to_utc

get_symbols = TestGetSymbols(unittest.TestCase);
get_symbols.test_request();
