import unittest
from unittest.mock import Mock, patch

from click.testing import CliRunner

from jhsingle_native_proxy import main


class MainOptionsTest(unittest.TestCase):
    @patch.object(main, "start_keep_alive")
    @patch.object(main.ioloop.IOLoop, "current")
    @patch.object(main, "HTTPServer")
    @patch.object(main, "get_ssl_options", return_value=None)
    @patch.object(main, "make_app", return_value=Mock(settings={}))
    @patch.object(main, "configure_http_client")
    def test_large_body_options_configure_tornado_server(
            self, configure_http_client, make_app, get_ssl_options,
            http_server, current_ioloop, start_keep_alive):
        server = http_server.return_value
        result = CliRunner().invoke(main.run, [
            "--port", "9999",
            "--last-activity-interval", "0",
            "--max-body-size", "2164260864",
            "--body-timeout", "1800",
            "python",
        ])

        self.assertEqual(result.exit_code, 0, result.output)
        http_server.assert_called_once_with(
            make_app.return_value,
            ssl_options=None,
            xheaders=True,
            max_body_size=2164260864,
            max_buffer_size=2164260864,
            body_timeout=1800,
        )
        server.listen.assert_called_once_with(9999, None)
        current_ioloop.return_value.start.assert_called_once_with()
        start_keep_alive.assert_not_called()


if __name__ == "__main__":
    unittest.main()
