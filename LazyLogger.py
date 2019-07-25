import inspect
import logging
from os.path import basename


class LazyLogger:
	logger: logging.Logger

	def __init__(self, logger: logging.Logger):
		self.logger = logger

	def get_logger(self):
		return self.logger

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

	@staticmethod
	def msg_format(calling_class, calling_method, msg):
		return f"{calling_class}.{calling_method}(): {msg}"

	@staticmethod
	def build_msg(stack, msg):
		return LazyLogger.msg_format(*LazyLogger.__gather_stack_info(stack), msg)

	def debug(self, msg, *args, **kwargs):
		self.logger.debug(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def info(self, msg, *args, **kwargs):
		self.logger.info(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def warning(self, msg, *args, **kwargs):
		self.logger.warning(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def warn(self, msg, *args, **kwargs):
		self.logger.warn(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		self.logger.error(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def exception(self, msg, *args, exc_info=True, **kwargs):
		self.logger.exception(self.build_msg(inspect.stack(), msg), *args, exc_info, **kwargs)

	def critical(self, msg, *args, **kwargs):
		self.logger.critical(self.build_msg(inspect.stack(), msg), *args, **kwargs)

	def log(self, level, msg, *args, **kwargs):
		self.logger.log(level, self.build_msg(inspect.stack(), msg), *args, **kwargs)
