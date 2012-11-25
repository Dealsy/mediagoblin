# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from mediagoblin.db.sql.base import Base

from sqlalchemy import (
    Column, Integer, Float, ForeignKey)
from sqlalchemy.orm import relationship, backref
from mediagoblin.db.sql.extratypes import JSONEncoded


class ImageData(Base):
    __tablename__ = "image__mediadata"

    # The primary key *and* reference to the main media_entry
    media_entry = Column(Integer, ForeignKey('core__media_entries.id'),
        primary_key=True)
    get_media_entry = relationship("MediaEntry",
        backref=backref("image__media_data", cascade="all, delete-orphan"))

    width = Column(Integer)
    height = Column(Integer)
    exif_all = Column(JSONEncoded)
    gps_longitude = Column(Float)
    gps_latitude = Column(Float)
    gps_altitude = Column(Float)
    gps_direction = Column(Float)

    def get_original_date(self):
        """
        Get the original date and time from the EXIF information. Returns
        either a datetime object or None (if anything goes wrong)
        """

        import datetime
        try:
            # Try wrapped around all since exif_all might be none,
            # EXIF DateTimeOriginal or printable might not exist, or
            # strptime might not be able to parse date correctly
            exif_date = self.exif_all['EXIF DateTimeOriginal']['printable']
            original_date = datetime.datetime.strptime(exif_date,
                                                       '%Y:%m:%d %H:%M:%S')
            return original_date
        except:
            return None

DATA_MODEL = ImageData
MODELS = [ImageData]
