from bot_code.conversions.input import input_formatter
import tensorflow as tf


class TensorflowInputFormatter(input_formatter.InputFormatter):
    def __init__(self, team, index, batch_size, feature_creator=None):
        """
        :param team: Which team the bot is on
        :param index: Which index is the bot inside the game_tick_packet
        :param batch_size: size of the batch
        :param feature_creator: used to create_features if features exist
        """
        super().__init__(team, index)
        self.batch_size = batch_size
        self.feature_creator = feature_creator

    def get_last_touched_ball(self, car, latest_touch):
        return tf.equal(car.wName, latest_touch.wPlayerName)

    def return_emtpy_player_array(self):
        """
        :return: An array representing a car with no data
        """
        array = []
        for i in range(len(super().return_emtpy_player_array())):
            array.append(tf.constant([0.0] * self.batch_size))
        return array

    def create_result_array(self, array):
        if self.feature_creator is not None:
            array += self.feature_creator.generate_features(array)
        converted_array = []
        for i in range(len(array)):
            casted_number = array[i]
            if array[i].dtype != tf.float32:
                casted_number = tf.cast(array[i], tf.float32)
            converted_array.append(casted_number)

        result = tf.stack(converted_array, axis=1)

        return result

    def create_input_array(self, game_tick_packet, passed_time=None):
        if passed_time is not None:
            return super().create_input_array(game_tick_packet, passed_time)
        return super().create_input_array(game_tick_packet, tf.constant([0.0] * self.batch_size))
