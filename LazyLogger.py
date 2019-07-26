import inspect
import logging
from os.path import basename


class LazyLogger:
	__logger: logging.Logger
	host_name: str

	def __init__(self, name: str = None, host_name: str = ""):
		self.__logger: logging.Logger = logging.getLogger(name)
		self.host_name = host_name + ": " if host_name else  ""

	def get_logger(self):
		return self.__logger

	@staticmethod
	def __gather_stack_info(stack):
		stack = stack[1]

		try:
			calling_class = stack[0].f_locals["self"].__class__.__name__
		except KeyError:
			calling_class = basename(inspect.getmodule(stack[0]).__file__)

		calling_method = stack.function

		if calling_method == '<module>':
			calling_method = '__main__'

		return calling_class, calling_method

	def msg_format(self, calling_class, calling_method, msg):
		return f"{self.host_name}{calling_class}.{calling_method}(): {msg}"

	def build_msg(self, stack, msg):
		return LazyLogger.msg_format(self, *LazyLogger.__gather_stack_info(stack), msg)

	def debug(self, msg, *args, **kwargs):
		self.__logger.debug(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def info(self, msg, *args, **kwargs):
		self.__logger.info(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def warning(self, msg, *args, **kwargs):
		self.__logger.warning(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def warn(self, msg, *args, **kwargs):
		self.__logger.warn(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		self.__logger.error(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def exception(self, msg, *args, exc_info=True, **kwargs):
		self.__logger.exception(self.build_msg(inspect.stack(), msg), *args, exc_info, **kwargs)

	def critical(self, msg, *args, **kwargs):
		self.__logger.critical(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def log(self, level, msg, *args, **kwargs):
		self.__logger.log(level, self.build_msg(inspect.stack(), msg), *args, **kwargs)
