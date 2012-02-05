# @INVIENT_COPYRIGHT@
# @MUNTJAC_LICENSE@
import datetime

from muntjac.ui.abstract_component \
    import AbstractComponent

from muntjac.addon.invient.invient_charts_config \
    import BaseLineConfig, PointConfig, SeriesConfig

from muntjac.addon.invient.invient_charts_util \
    import InvientChartsUtil


class InvientCharts(AbstractComponent):
    """A Vaddin component representing charts. It is a the main class of
    InvientCharts library.

    A chart typically contains one or more series of same or different types.
    This class allows us to specify series of different types say line and pie
    and hence it makes it easy to build a combination chart.

    After a chart L{InvientCharts} is created, the following changes to the
    chart will be reflected rendered on the webkit.

      * Set or update chart {@link Title} and/or {@link SubTitle}</li>
      * Modify chart size</li>
      * Add, update and remove one or more instances of {@link PlotBand} and
    {@link PlotLine}</li>
      * Set or update axis categories</li>
      * Set or update axis min and max values</li>
      * Add, update and remove one or more instances of {@link Series}</li>
      * Show or hide one or more instances of {@link Series}</li>
      * Add and remove one or more instances of {@link Point}</li>
      * Register and unregister event listeners</li>

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, chartConfig):
        """Creates this chart object with given chart configuration

        @param chartConfig
        """
        if chartConfig is None:
            raise ValueError('The chart cannot be created without '
                    'chartConfig argument.')
        self._chartConfig = chartConfig
        self._chartConfig.setInvientCharts(self)

        self._isRetrieveSVG = False
        self._isPrint = False

        self._pointClickListeners = dict()
        self._pointRemoveListeners = dict()
        self._pointUnselectListeners = dict()
        self._pointSelectListeners = dict()
        self._seriesClickListeners = dict()
        self._seriesHideListeners = dict()
        self._seriesShowListeners = dict()
        self._seriesLegendItemClickListeners = dict()
        self._pieChartLegendItemClickListener = set()
        self._chartClickListener = set()
        self._chartAddSeriesListener = set()
        self._chartZoomListener = set()
        self._chartResetZoomListener = set()
        self._svgAvailableListener = None
        self._chartSeries = set()
        self._reloadChartSeries = False


    def getConfig(self):
        """Returns chart configuration object

        @return: Returns chart configuration object
        """
        return self._chartConfig


    def paintContent(self, target):
        super(InvientCharts, self).paintContent(target)

        # Update all series with reference of x and y axis.
        self.setAxisInAllSeriesIfNotSetAlready()

        # Configurations options
        target.startTag('options')
        if self._chartConfig is not None:
            InvientChartsUtil.writeTitleConfig(target, self._chartConfig.getTitle())
            InvientChartsUtil.writeSubtitleConfig(target, self._chartConfig.getSubtitle())
            InvientChartsUtil.writeCreditConfig(target, self._chartConfig.getCredit())
            InvientChartsUtil.writeLegendConfig(target, self._chartConfig.getLegend())
            InvientChartsUtil.writeTooltipConfig(target, self._chartConfig.getTooltip())
            InvientChartsUtil.writeGeneralChartConfig(target, self._chartConfig.getGeneralChartConfig())
            InvientChartsUtil.writeSeriesConfigPerSeriesType(target, self._chartConfig.getSeriesConfig())
            InvientChartsUtil.writeXAxes(target, self._chartConfig.getXAxes(), self._chartConfig)
            InvientChartsUtil.writeYAxes(target, self._chartConfig.getYAxes(), self._chartConfig)
            InvientChartsUtil.writeChartLabelConfig(target, self._chartConfig.getChartLabel())
        target.endTag('options')
        target.startTag('chartData')

        InvientChartsUtil.writeSeries(target,
                self._chartConfig.getGeneralChartConfig().getType(),
                self._chartSeries,
                self._chartConfig.getXAxes(),
                self._chartConfig.getYAxes())
        target.endTag('chartData')

        # A flag to indicate whether to retrieve svg from client or not.
        target.addAttribute('isRetrieveSVG', self._isRetrieveSVG)

        # A flag to indicate whether to prompt print dialog on client or not
        target.addAttribute('isPrint', self._isPrint)

        # Events
        target.startTag('events')

        # Chart Events
        self.paintChartEvents(target)

        # Series/Point Events
        self.paintSeriesAndPointEvents(target)
        target.endTag('events')

        # If the flag reloadChartData is true then the
        # client will ignore seriesOperations and
        # remove all existing series of a chart and
        # add series info received from the server.
        target.addAttribute('reloadChartSeries', self._reloadChartSeries)
        target.startTag('chartDataUpdates')
        if not self._reloadChartSeries:
            InvientChartsUtil.writeChartDataUpdates(target, self._seriesCURMap)
        target.endTag('chartDataUpdates')

        # reset flag
        self._reloadChartSeries = False

        # reset series operations
        self._seriesCURMap.clear()

        # reset to not retrieve svg when other updates on the chart occurs.
        # The svg is retrieved only when a svg available listener is registered
        # on this chart
        self._isRetrieveSVG = False
        self._isPrint = False


    def paintChartEvents(self, target):
        target.startTag('chartEvents')
        if (self._chartAddSeriesListener is not None
                and len(self._chartAddSeriesListener) > 0):
            target.addAttribute('addSeries', True)
        if (self._chartClickListener is not None
                and len(self._chartClickListener) > 0):
            target.addAttribute('click', True)
        if (self._chartZoomListener is not None
                and len(self._chartZoomListener) > 0):
            target.addAttribute('selection', True)
        target.endTag('chartEvents')


    def paintSeriesAndPointEvents(self, target):
        target.startTag('seriesEvents')
        # For each series type, check if listeners exist. If so then add.
        for seriesType in self.SeriesType.values():
            self.paintSeriesEvents(target, seriesType)
        target.endTag('seriesEvents')


    def paintSeriesEvents(self, target, seriesType):
        tagName = seriesType.getName()
        target.startTag(tagName)
        if (seriesType in self._seriesClickListeners
                and len(self._seriesClickListeners[seriesType]) > 0):
            target.addAttribute('click', True)
        if (seriesType in self._seriesHideListeners
                and len(self._seriesHideListeners[seriesType]) > 0):
            target.addAttribute('hide', True)
        if (seriesType in self._seriesShowListeners
                and len(self._seriesShowListeners[seriesType]) > 0):
            target.addAttribute('show', True)
        if (seriesType in self._seriesLegendItemClickListeners
                and len(self._seriesLegendItemClickListeners[seriesType]) > 0):
            target.addAttribute('legendItemClick', True)

        # Check for point events
        self.paintPointEvents(target, seriesType)
        target.endTag(tagName)


    def paintPointEvents(self, target, seriesType):
        target.startTag('pointEvents')
        if (seriesType in self._pointClickListeners
                and len(self._pointClickListeners[seriesType]) > 0):
            target.addAttribute('click', True)
        if (seriesType in self._pointRemoveListeners
                and len(self._pointRemoveListeners[seriesType]) > 0):
            target.addAttribute('remove', True)
        if (seriesType in self._pointSelectListeners
                and len(self._pointSelectListeners[seriesType]) > 0):
            target.addAttribute('select', True)
        if (seriesType in self._pointUnselectListeners
                and len(self._pointUnselectListeners[seriesType]) > 0):
            target.addAttribute('unselect', True)
        # Event applicable only for pie chart
        if (SeriesType.PIE == seriesType
                and len(self._pieChartLegendItemClickListener) > 0):
            target.addAttribute('legendItemClick', True)
        target.endTag('pointEvents')


    def changeVariables(self, source, variables):
        if 'event' in variables:
            eventData = variables['eventData']
            eventName = variables['event']
            if eventName.lower() == "addSeries".lower():
                self.fireAddSeries()
            elif eventName.lower() == "chartClick".lower():
                xAxisPos = float(eventData.get("xAxisPos"))
                yAxisPos = float(eventData.get("yAxisPos"))
                ##
                mousePosition = self.getClickPosition(eventData)
                self.fireChartClick(DecimalPoint(xAxisPos, yAxisPos),
                        mousePosition)
            elif eventName.lower() == "chartZoom".lower():
                xAxisMin = float(eventData.get("xAxisMin"))
                xAxisMax = float(eventData.get("xAxisMax"))
                yAxisMin = float(eventData.get("yAxisMin"))
                yAxisMax = float(eventData.get("yAxisMax"))
                self.fireChartZoom(ChartArea(xAxisMin, xAxisMax, yAxisMin,
                        yAxisMax))
            elif eventName.lower() == "chartResetZoom".lower():
                self.fireChartResetZoom()
            elif eventName.lower() == "chartSVGAvailable".lower():
                self.fireChartSVGAvailable(eventData.get("svg"))
            elif eventName.lower() == "seriesClick".lower():
                pointEventData = self.getPointEventData(eventData)
                ##
                mousePosition = self.getClickPosition(eventData)
                self.fireSeriesClick(
                        self.getSeriesFromEventData(pointEventData.getSeriesName()),
                        self.getPointFromEventData(pointEventData), mousePosition)
            elif eventName.lower() == "seriesHide".lower():
                seriesName = eventData.get("seriesName")
                self.fireSeriesHide(self.getSeriesFromEventData(seriesName))
            elif eventName.lower() == "seriesShow".lower():
                seriesName = eventData.get("seriesName")
                self.fireSeriesShow(self.getSeriesFromEventData(seriesName))
            elif eventName.lower() == "seriesLegendItemClick".lower():
                seriesName = eventData.get("seriesName")
                self.fireSeriesLegendItemClick(self.getSeriesFromEventData(seriesName))
            elif eventName.lower() == "pieLegendItemClick".lower():
                pointEventData = self.getPointEventData(eventData)
                self.fireLegendItemClick(self.getPointFromEventData(pointEventData))
            elif eventName.lower() == "pointClick".lower():
                mousePosition = self.getClickPosition(eventData)
                ##
                pointEventData = self.getPointEventData(eventData)
                self.firePointClick(pointEventData.getCategory(),
                        self.getPointFromEventData(pointEventData), mousePosition)
            elif eventName.lower() == "pointSelect".lower():
                pointEventData = self.getPointEventData(eventData)
                self.firePointSelect(pointEventData.getCategory(),
                        self.getPointFromEventData(pointEventData))
            elif eventName.lower() == "pointUnselect".lower():
                pointEventData = self.getPointEventData(eventData)
                self.firePointUnselect(pointEventData.getCategory(),
                        self.getPointFromEventData(pointEventData))
            elif eventName.lower() == "pointRemove".lower():
                pointEventData = self.getPointEventData(eventData)
                self.firePointRemove(pointEventData.getCategory(),
                        self.getPointFromEventData(pointEventData))


    def getPointFromEventData(self, eventData):
        # First locate a series and then point
        series = self.getSeriesFromEventData(eventData.getSeriesName())
        if series is not None:
            if isinstance(series, self.XYSeries):
                for point in series.getPoints():
                    if (point.getY() is not None
                        and point.getY().compareTo(eventData.getPointY()) == 0
                        and point.getX() is not None
                        and point.getX().compareTo(eventData.getPointX()) == 0):
                        return point
            else:
                for point in series.getPoints():
                    if (point.getY() is not None
                        and point.getY().compareTo(eventData.getPointY()) == 0
                        and point.getX() is not None
                        and self.getDateInMilliseconds(point.getX(),
                                series.isIncludeTime()) == eventData.getPointX()):
                        return point
        return None


    @classmethod
    def getDateInMilliseconds(cls, dt, isIncludeTime):
        if dt is None:
            return None
        cal = GregorianCalendar.getInstance()
        cal.setTime(dt)
        if not isIncludeTime:
            cal.set(Calendar.HOUR, 0)
            cal.set(Calendar.MINUTE, 0)
            cal.set(Calendar.SECOND, 0)
            cal.set(Calendar.MILLISECOND, 0)
        return cal.getTimeInMillis()


    def getSeriesFromEventData(self, seriesName):
        for series in self._chartSeries:
            if series.getName() == seriesName:
                return series
        # Should not happen
        # If it happens then why? Any comments???
        return None


    def fireAddSeries(self):
        self.fireEvent(ChartAddSeriesEvent(self, self))


    def fireChartClick(self, point, mousePosition):
        self.fireEvent(ChartClickEvent(self, self, point, mousePosition))


    def fireChartZoom(self, selectedArea):
        self.fireEvent(ChartZoomEvent(self, self, selectedArea))


    def fireChartSVGAvailable(self, svg):
        self.fireEvent(ChartSVGAvailableEvent(self, self, svg))


    def fireChartResetZoom(self):
        self.fireEvent(ChartResetZoomEvent(self, self))


    def fireSeriesClick(self, series, point, mousePosition):
        self.fireEvent(SeriesClickEvent(self, self, series, point, mousePosition))


    def fireSeriesShow(self, series):
        self.fireEvent(SeriesShowEvent(self, self, series))


    def fireSeriesHide(self, series):
        self.fireEvent(SeriesHideEvent(self, self, series))


    def fireSeriesLegendItemClick(self, series):
        self.fireEvent(SeriesLegendItemClickEvent(self, self, series))


    def firePointClick(self, category, point, mousePosition):
        self.fireEvent(PointClickEvent(self, self, category, point, mousePosition))


    def firePointSelect(self, category, point):
        self.fireEvent(PointSelectEvent(self, self, category, point))


    def firePointUnselect(self, category, point):
        self.fireEvent(PointUnselectEvent(self, self, category, point))


    def firePointRemove(self, category, point):
        self.fireEvent(PointRemoveEvent(self, self, category, point))


    def fireLegendItemClick(self, point):
        self.fireEvent(PieChartLegendItemClickEvent(self, self, point))


    def getPointEventData(self, eventData):
        seriesName = eventData['seriesName']
        category = eventData['category']
        pointX = float(eventData['pointX'])
        pointY = float(eventData['pointY'])
        return PointEventData(seriesName, category, pointX, pointY)


    def getClickPosition(self, eventData):
        mouseX = None
        if isinstance(eventData['mouseX'], int):
            mouseX = eventData['mouseX']
        mouseY = None
        if isinstance(eventData['mouseY'], int):
            mouseY = eventData['mouseY']
        if mouseX is not None and mouseY is not None:
            return MousePosition(mouseX, mouseY)
        return None


    def addListener(self, listener, seriesTypes=None):
        """Adds the point click listener. If the argument seriesTypes is not
        specified then the listener will be added for all series type otherwise
        it will be added for a specific series type

        @param listener
                   the Listener to be added.
        ---
        Adds the point remove listener. If the argument seriesTypes is not
        specified then the listener will be added for all series type otherwise
        it will be added for a specific series type

        @param listener
                   the Listener to be added.
        ---
        Adds the point unselect listener. If the argument seriesTypes is not
        specified then the listener will be added for all series type otherwise
        it will be added for a specific series type

        @param listener
                   the Listener to be added.
        ---
        Adds the point select listener. If the argument seriesTypes is not
        specified then the listener will be added for all series type otherwise
        it will be added for a specific series type

        @param listener
                   the Listener to be added.
        ---
        Adds the series click listener. If the argument seriesTypes is not
        specified then the listener will be added for all series type otherwise
        it will be added for a specific series type

        @param listener
                   the Listener to be added.
        ---
        Adds the series hide listener. If the argument seriesTypes is not
        specified then the listener will be added for all series type otherwise
        it will be added for a specific series type

        @param listener
                   the Listener to be added.
        ---
        Adds the series show listener. If the argument seriesTypes is not
        specified then the listener will be added for all series type otherwise
        it will be added for a specific series type

        @param listener
                   the Listener to be added.
        ---
        Adds the series legend item click listener. If the argument seriesTypes
        is not specified then the listener will be added for all series type
        otherwise it will be added for a specific series type

        @param listener
                   the Listener to be added.
        ---
        Adds the piechart legend item click listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the chart click listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the series add listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the chart zoom listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the chart reset zoom listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the chart svg available listener for this chart. If the chart
        already has a listener of this type then the existing listener will be
        removed and the argument listener will be registered.

        @param listener
                   the Listener to be added or registered.
        """
        if seriesTypes is None:
            if isinstance(listener, ChartAddSeriesListener):
                self._chartAddSeriesListener.add(listener)
                self.addListener(ChartAddSeriesEvent, listener,
                                 self._CHART_ADD_SERIES_METHOD)
            elif isinstance(listener, ChartClickListener):
                self._chartClickListener.add(listener)
                self.addListener(ChartClickEvent, listener, self._CHART_CLICK_METHOD)
            elif isinstance(listener, ChartResetZoomListener):
                self._chartResetZoomListener.add(listener)
                self.addListener(ChartResetZoomEvent, listener, self._CHART_RESET_ZOOM_METHOD)
            elif isinstance(listener, ChartSVGAvailableListener):
                if (self._svgAvailableListener is not None
                        and self._svgAvailableListener != listener):
                    # remove earlier listener
                    self.removeListener(self._svgAvailableListener)
                self._svgAvailableListener = listener
                self.addListener(ChartSVGAvailableEvent, self._svgAvailableListener, self._CHART_SVG_AVAILABLE_METHOD)
                self._isRetrieveSVG = True
                self.requestRepaint()
            elif isinstance(listener, ChartZoomListener):
                self._chartZoomListener.add(listener)
                self.addListener(ChartZoomEvent, listener, self._CHART_ZOOM_METHOD)
            else:
                self._pieChartLegendItemClickListener.add(listener)
                self.addListener(PieChartLegendItemClickEvent, listener, self._LEGENDITEM_CLICK_METHOD)
        else:
            if isinstance(listener, PointClickListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointClickListeners:
                        self._pointClickListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._pointClickListeners[seriesType] = listeners
                self.addListener(PointClickEvent, listener, _POINT_CLICK_METHOD)
            elif isinstance(listener, PointRemoveListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointRemoveListeners:
                        self._pointRemoveListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._pointRemoveListeners[seriesType] = listeners
                self.addListener(PointRemoveEvent, listener, _POINT_REMOVE_METHOD)
            elif isinstance(listener, PointSelectListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointSelectListeners:
                        self._pointSelectListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._pointSelectListeners.put(seriesType, listeners)
                self.addListener(PointSelectEvent, listener, _POINT_SELECT_METHOD)
            elif isinstance(listener, PointUnselectListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointUnselectListeners:
                        self._pointUnselectListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._pointUnselectListeners.put(seriesType, listeners)
                self.addListener(PointUnselectEvent, listener, _POINT_UNSELECT_METHOD)
            elif isinstance(listener, SeriesClickListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesClickListeners:
                        self._seriesClickListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._seriesClickListeners[seriesType] = listeners
                self.addListener(SeriesClickEvent, listener, _SERIES_CLICK_METHOD)
            elif isinstance(listener, SeriesHideListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesHideListeners:
                        self._seriesHideListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._seriesHideListeners[seriesType] = listeners
                self.addListener(SeriesHideEvent, listener, _SERIES_HIDE_METHOD)
            elif isinstance(listener, SeriesLegendItemClickListerner):
                if seriesTypes.length == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesLegendItemClickListeners:
                        self._seriesLegendItemClickListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._seriesLegendItemClickListeners[seriesType] = listeners
                self.addListener(self.SeriesLegendItemClickEvent, listener, _SERIES_LEGENDITEM_CLICK_METHOD)
            else:
                if seriesTypes.length == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesShowListeners:
                        self._seriesShowListeners[seriesType].add(listener)
                    else:
                        listeners = set()
                        listeners.add(listener)
                        self._seriesShowListeners[seriesType] = listeners
                self.addListener(SeriesShowEvent, listener, _SERIES_SHOW_METHOD)


    def removeListener(self, listener, seriesTypes=None):
        """Removes the point click listener. If the argument seriesTypes is not
        specified then the listener will be removed only for a series type
        SeriesType.COMMONSERIES otherwise the listener will be removed for all
        specified series types.

        @param listener
                   the listener to be removed
        @param seriesTypes
                   one or more series types as defined by (@link SeriesType}
        ---
        Removes the point remove listener. If the argument seriesTypes is not
        specified then the listener will be removed only for a series type
        SeriesType.COMMONSERIES otherwise the listener will be removed for all
        specified series types.

        @param listener
                   the listener to be removed
        @param seriesTypes
                   one or more series types as defined by (@link SeriesType}
        ---
        Removes the point unselect listener. If the argument seriesTypes is not
        specified then the listener will be removed only for a series type
        SeriesType.COMMONSERIES otherwise the listener will be removed for all
        specified series types.

        @param listener
                   the listener to be removed
        @param seriesTypes
                   one or more series types as defined by (@link SeriesType}
        ---
        Removes the point select listener. If the argument seriesTypes is not
        specified then the listener will be removed only for a series type
        SeriesType.COMMONSERIES otherwise the listener will be removed for all
        specified series types.

        @param listener
                   the listener to be removed
        @param seriesTypes
                   one or more series types as defined by (@link SeriesType}
        ---
        Removes the series click listener. If the argument seriesTypes is not
        specified then the listener will be removed only for a series type
        SeriesType.COMMONSERIES otherwise the listener will be removed for all
        specified series types.

        @param listener
                   the listener to be removed
        @param seriesTypes
                   one or more series types as defined by (@link SeriesType}
        ---
        Removes the series hide listener. If the argument seriesTypes is not
        specified then the listener will be removed only for a series type
        SeriesType.COMMONSERIES otherwise the listener will be removed for all
        specified series types.

        @param listener
                   the listener to be removed
        @param seriesTypes
                   one or more series types as defined by (@link SeriesType}
        ---
        Removes the series show listener. If the argument seriesTypes is not
        specified then the listener will be removed only for a series type
        SeriesType.COMMONSERIES otherwise the listener will be removed for all
        specified series types.

        @param listener
                   the listener to be removed
        @param seriesTypes
                   one or more series types as defined by (@link SeriesType}
        ---
        Removes the series legend item click listener. If the argument
        seriesTypes is not specified then the listener will be removed only for a
        series type SeriesType.COMMONSERIES otherwise the listener will be
        removed for all specified series types.

        @param listener
                   the listener to be removed
        @param seriesTypes
                   one or more series types as defined by (@link SeriesType}
        ---
        Removes the piechart legend item click listener.

        @param listener
                   the listener to be removed
        ---
        Removes the chart click listener.

        @param listener
                   the listener to be removed
        ---
        Removes the series add listener.

        @param listener
                   the listener to be removed
        ---
        Removes the chart zoom listener.

        @param listener
                   the listener to be removed
        ---
        Removes the chart reset zoom listener.

        @param listener
                   the listener to be removed
        ---
        Removes the chart svg available listener for this chart.

        @param listener
                   the listener to be removed or unregistered.
        """
        if seriesTypes is None:
            if isinstance(listener, ChartAddSeriesListener):
                self._chartAddSeriesListener.remove(listener)
                self.removeListener(ChartAddSeriesEvent, listener, self._CHART_ADD_SERIES_METHOD)
            elif isinstance(listener, ChartClickListener):
                self._chartClickListener.remove(listener)
                self.removeListener(ChartClickEvent, listener, self._CHART_CLICK_METHOD)
            elif isinstance(listener, ChartResetZoomListener):
                self._chartResetZoomListener.remove(listener)
                self.removeListener(ChartResetZoomEvent, listener, self._CHART_RESET_ZOOM_METHOD)
            elif isinstance(listener, ChartSVGAvailableListener):
                if self._svgAvailableListener == listener:
                    self.removeListener(ChartSVGAvailableEvent, listener, self._CHART_SVG_AVAILABLE_METHOD)
                    self._isRetrieveSVG = False
                    self._svgAvailableListener = None
            elif isinstance(listener, ChartZoomListener):
                self._chartZoomListener.remove(listener)
                self.removeListener(ChartZoomEvent, listener, self._CHART_ZOOM_METHOD)
            else:
                self._pieChartLegendItemClickListener.remove(listener)
                self.removeListener(PieChartLegendItemClickEvent, listener, self._LEGENDITEM_CLICK_METHOD)
        else:
            if isinstance(listener, PointClickListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointClickListeners:
                        self._pointClickListeners[seriesType].remove(listener)
                self.removeListener(PointClickEvent, listener, _POINT_CLICK_METHOD)
            elif isinstance(listener, PointRemoveListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointRemoveListeners:
                        self._pointRemoveListeners[seriesType].remove(listener)
                self._pointRemoveListeners.remove(listener)
                self.removeListener(PointRemoveEvent, listener, _POINT_REMOVE_METHOD)
            elif isinstance(listener, PointSelectListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointSelectListeners:
                        self._pointSelectListeners[seriesType].remove(listener)
                self.removeListener(PointSelectEvent, listener, _POINT_SELECT_METHOD)
            elif isinstance(listener, PointUnselectListener):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._pointUnselectListeners:
                        self._pointUnselectListeners[seriesType].remove(listener)
                self.removeListener(PointUnselectEvent, listener, _POINT_UNSELECT_METHOD)
            elif isinstance(listener, SeriesClickListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesClickListeners:
                        self._seriesClickListeners[seriesType].remove(listener)
                self.removeListener(SeriesClickEvent, listener, _SERIES_CLICK_METHOD)
            elif isinstance(listener, SeriesHideListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesHideListeners:
                        self._seriesHideListeners[seriesType].remove(listener)
                self.removeListener(SeriesHideEvent, listener, _SERIES_HIDE_METHOD)
            elif isinstance(listener, SeriesLegendItemClickListerner):
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesLegendItemClickListeners:
                        self._seriesLegendItemClickListeners[seriesType].remove(listener)
                self.removeListener(SeriesLegendItemClickEvent, listener, _SERIES_LEGENDITEM_CLICK_METHOD)
            else:
                if len(seriesTypes) == 0:
                    seriesTypes = [SeriesType.COMMONSERIES]
                for seriesType in seriesTypes:
                    if seriesType in self._seriesShowListeners:
                        self._seriesShowListeners[seriesType].remove(listener)
                self.removeListener(SeriesShowEvent, listener, _SERIES_SHOW_METHOD)


    def setSeries(self, series):
        """The data of a chart is defined in terms of L{Series}. This method
        removes all previously set series of this chart and adds the argument
        series. If the argument series is null then no actions are taken.

        @param series:
                   A collection of series to set as chart's data
        """
        if series is not None:
            self._reloadChartSeries = True
            self._chartSeries.clear()
            self._seriesCURMap.clear()
            for seriesData in series:
                self.addSeries(seriesData)


    def getSeries(self, name):
        """Returns a series whose name matches the argument name.

        @param name:
                   the name of the series
        @return: Returns a series with the given name
        """
        for series in self._chartSeries:
            if series.getName() == name:
                return series
        return None


    def getAllSeries(self):
        """Returns all series associated with this chart.
        @return: returns all series associated with this chart.
        """
        return self._chartSeries


    def addSeries(self, seriesData):
        """Adds the argument series to this chart.

        @param seriesData:
                   the series to be added
        """
        # Before sending data to the client, this method sets
        # axis in all series associated with the chart
        if self._chartSeries.add(seriesData):
            self.setAxisInSeriesIfNotSetAlready(seriesData)
            seriesData.setInvientCharts(self)
            self.addSeriesCUROperation(SeriesCUR(SeriesCURType.ADD, seriesData.getName()))
            self.requestRepaint()


    def setAxisInAllSeriesIfNotSetAlready(self):
        for series in self._chartSeries:
            self.setAxisInSeriesIfNotSetAlready(series)


    def setAxisInSeriesIfNotSetAlready(self, series):
        if self.getConfig() is not None:
            if (series.getXAxis() is None
                    and self.getConfig().getXAxes() is not None
                    and len(self.getConfig().getXAxes()) > 0):
                series.setXAxis(self.getConfig().getXAxes().next())
            if (series.getYAxis() is None
                    and self.getConfig().getYAxes() is not None
                    and len(self.getConfig().getYAxes()) > 0):
                series.setYAxis(self.getConfig().getYAxes().next())


    def removeSeries(self, name_or_seriesData):
        """Removes a series whose name matches the argument name or the
        argument seriesData from this chart.

        @param seriesData:
                   the name of the series or the series object to be removed
        """
        if isinstance(name_or_seriesData, Series):
            seriesData = name_or_seriesData
            if self._chartSeries.remove(seriesData):  ## FIXME: remove
                seriesData.setInvientCharts(None)
                self.addSeriesCUROperation(SeriesCUR(SeriesCURType.REMOVE, seriesData.getName()))
                self.requestRepaint()
        else:
            name = name_or_seriesData

            seriesItr = self._chartSeries
            for series in seriesItr:
                if series.getName() == name:
                    seriesItr.remove()
                    series.setInvientCharts(None)
                    self.addSeriesCUROperation(SeriesCUR(SeriesCURType.REMOVE, series.getName()))
                    self.requestRepaint()






    def DateTimePoint(InvientCharts_this, *args, **kwargs):

        return DateTimePoint(*args, **kwargs)

    def Series(InvientCharts_this, *args, **kwargs):

        return Series(*args, **kwargs)

    def XYSeries(InvientCharts_this, *args, **kwargs):

        class XYSeries(Series):
            """This class defines a number series. In this series both X and Y values
            must be number. To use date values, use {@link DateTimeSeries}

            @author Invient

            @see DateTimeSeries
            """

            def __init__(self, *args):
                """Creates a series with given name

                @param name
                           the name of this series
                ---
                Creates a series with given name and configuration

                @param name
                           the name of this series
                @param config
                           the configuration for this series
                ---
                Creates a series with given name and type

                @param name
                           the name of this series
                @param seriesType
                           the type of this series
                ---
                Creates a series with given name, type and configuration

                @param name
                           the name of this series
                @param seriesType
                           the type of this series
                @param config
                           the configuration for this series
                """
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    name, = _0
                    super(XYSeries, self)(name)
                elif _1 == 2:
                    if isinstance(_0[1], InvientCharts_this.SeriesType):
                        name, seriesType = _0
                        super(XYSeries, self)(name, seriesType)
                    else:
                        name, config = _0
                        super(XYSeries, self)(name, config)
                elif _1 == 3:
                    name, seriesType, config = _0
                    super(XYSeries, self)(name, seriesType, config)
                else:
                    raise ARGERROR(1, 3)

            def removePoint(self, *points):
                """Removes the specified point from the series

                @param points
                """
                # (non-Javadoc)
                #
                # @see com.invient.vaadin.chart.InvientChart.Series#removeAllPoints()

                super(XYSeries, self).removePoint(points)

            def removeAllPoints(self):
                super(XYSeries, self).removeAllPoints()

            def addPoint(self, *args):
                """Appends the specified point into the series if they do not exists in
                this series. The points which already exists will not be appended. A
                collection of points appended to this series will be returned.

                @param points
                @return Returns a collection of points which are added in this
                        series. If a point has same (x, y) value as any other point
                        in the input argument points then it will not be added in
                        this series.
                ---
                Append the specified point into this series. If the argument shift is
                true then one point is shifted off the start of this series as one is
                appended to the end.

                @param points
                @param shift
                           If true then one point is shifted off the start of this
                           series as one is appended to the end.
                @return Returns a collection of points which are added in this
                        series. If a point has same (x, y) value as any other point
                        in the input argument points then it will not be added in
                        this series.
                """
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    points, = _0
                    return super(XYSeries, self).addPoint(False, points)
                elif _1 == 2:
                    point, shift = _0
                    point.setShift(shift)
                    return super(XYSeries, self).addPoint(shift, point)
                else:
                    raise ARGERROR(1, 2)

            # (non-Javadoc)
            #
            # @see com.invient.vaadin.chart.InvientChart.Series#getPoints()

            def getPoints(self):
                return super(XYSeries, self).getPoints()

            def setSeriesPoints(self, points):
                """Sets points into this series. This method removes all of its points
                and then add points specified in the method argument. If the argument
                is null then no actions are taken.

                @param points
                           the collection of points to set into this series.
                @return Returns a collection of points which are set in this series.
                        If a point has same (x, y) value as any other point in the
                        argument points then it will not be added.
                """
                return super(XYSeries, self).setPoints(points)

            def updatePointXValuesIfNotPresent(self):
                pointStart = 0
                pointInterval = 1
                if isinstance(super(XYSeries, self).getConfig(), BaseLineConfig):
                    config = super(XYSeries, self).getConfig()
                    if config.getPointStart() is not None:
                        pointStart = config.getPointStart()
                    if config.getPointInterval() is not None:
                        pointInterval = config.getPointInterval()
                count = 0
                for point in self.getPoints():
                    if (point.getX() is None) or (point.getX() is not None and point.isAutosetX()):
                        point.setAutosetX(True)
                        if count == 0:
                            point.setX(pointStart)
                            count += 1
                        else:
                            pointStart = pointStart + pointInterval
                            point.setX(pointStart)

        return XYSeries(*args, **kwargs)

    def DateTimeSeries(InvientCharts_this, *args, **kwargs):

        class DateTimeSeries(Series):
            """This class defines a datetime series. In this series, the X value must be
            date and Y values must be number. To use number values, use
            {@link XYSeries}
            <p>
            By default, the time of a day is not included in the X value. In order to
            include time, use a constructor with argument isIncludeTime and pass true
            value for the argument.

            @author Invient

            @see XYSeries
            """
            _includeTime = None

            def __init__(self, *args):
                """Creates a series with given name. This series will not consider time
                in the X property of {@link DateTimePoint}. To include time, use any
                constructor having isIncludeTime as part of the arguments.

                @param name
                           the name of this series
                ---
                Creates a series with given name and boolean value.

                @param name
                           the name of this series
                @param isIncludeTime
                           If true then the time in the X property of
                           {@link DateTimePoint} will be considered when drawing the
                           chart. Defaults to false.
                ---
                Creates a series with given name and configuration.

                @param name
                           the name of this series
                @param config
                           the configuration for this series
                ---
                Creates a series with given name, configuration and boolean value.

                @param name
                           the name of this series
                @param config
                           the configuration for this series
                @param isIncludeTime
                           If true then the time in the X property of
                           {@link DateTimePoint} will be considered when drawing the
                           chart. Defaults to false.
                ---
                Creates a series with given name and type.

                @param name
                           the name of this series
                @param seriesType
                           the type of this series
                ---
                Creates a series with given name, type and boolean value.

                @param name
                           the name of this series
                @param seriesType
                           the type of this series
                @param isIncludeTime
                           If true then the time in the X property of
                           {@link DateTimePoint} will be considered when drawing the
                           chart. Defaults to false.
                ---
                Creates a series with given name, type and configuration.

                @param name
                           the name of this series
                @param seriesType
                           the type of this series
                @param config
                           the configuration for this series
                ---
                Creates a series with given name, type, configuration and boolean
                value.

                @param name
                           the name of this series
                @param seriesType
                           the type of this series
                @param config
                           the configuration for this series
                @param isIncludeTime
                           If true then the time in the X property of
                           {@link DateTimePoint} will be considered when drawing the
                           chart. Defaults to false.
                """
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    name, = _0
                    self.__init__(name, False)
                elif _1 == 2:
                    if isinstance(_0[1], InvientCharts_this.SeriesType):
                        name, seriesType = _0
                        self.__init__(name, seriesType, False)
                    elif isinstance(_0[1], SeriesConfig):
                        name, config = _0
                        self.__init__(name, config, False)
                    else:
                        name, isIncludeTime = _0
                        super(DateTimeSeries, self)(name)
                        self._includeTime = isIncludeTime
                elif _1 == 3:
                    if isinstance(_0[1], InvientCharts_this.SeriesType):
                        if isinstance(_0[2], SeriesConfig):
                            name, seriesType, config = _0
                            self.__init__(name, seriesType, config, False)
                        else:
                            name, seriesType, isIncludeTime = _0
                            super(DateTimeSeries, self)(name, seriesType)
                            self._includeTime = isIncludeTime
                    else:
                        name, config, isIncludeTime = _0
                        super(DateTimeSeries, self)(name, config)
                        self._includeTime = isIncludeTime
                elif _1 == 4:
                    name, seriesType, config, isIncludeTime = _0
                    super(DateTimeSeries, self)(name, seriesType, config)
                    self._includeTime = isIncludeTime
                else:
                    raise ARGERROR(1, 4)

            def removePoint(self, *points):
                """Removes all points specified as method argument into this series

                @param points
                """
                # (non-Javadoc)
                #
                # @see com.invient.vaadin.chart.InvientChart.Series#removeAllPoints()

                super(DateTimeSeries, self).removePoint(points)

            def removeAllPoints(self):
                super(DateTimeSeries, self).removeAllPoints()

            def addPoint(self, *args):
                """Appends the specified point into the series if they do not exists in
                this series. The points which already exists will not be appended. A
                collection of points appended to this series will be returned.

                @param points
                @return Returns a collection of points which are added in this
                        series. If a point has same (x, y) value as any other point
                        in the input argument points then it will not be added in
                        this series.
                ---
                Append the specified point into this series. If the argument shift is
                true then one point is shifted off the start of this series as one is
                appended to the end.

                @param point
                           A point to be added at the end of this series
                @param shift
                           If true then one point is shifted off the start of this
                           series as one is appended to the end.
                @return Returns a collection of points which are added in this
                        series. If a point has same (x, y) value as any other point
                        in the input argument points then it will not be added in
                        this series.
                """
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    points, = _0
                    return super(DateTimeSeries, self).addPoint(False, points)
                elif _1 == 2:
                    point, shift = _0
                    point.setShift(shift)
                    return super(DateTimeSeries, self).addPoint(shift, point)
                else:
                    raise ARGERROR(1, 2)

            def isIncludeTime(self):
                """@return Returns true if the time in the X property of
                        {@link DateTimePoint} will be considered when drawing the
                        chart otherwise false.
                """
                # (non-Javadoc)
                #
                # @see com.invient.vaadin.chart.InvientChart.Series#getPoints()

                return self._includeTime

            def getPoints(self):
                return super(DateTimeSeries, self).getPoints()

            def setSeriesPoints(self, points):
                """Sets points into this series. This method removes all of its points
                and then add points specified in the method argument. If the argument
                is null then no actions are taken.

                @param points
                           the collection of points to set into this series.
                @return Returns a collection of points which are added in this
                        series. If a point has same (x, y) value as any other point
                        in the input argument points then it will not be added in
                        this series.
                """
                return super(DateTimeSeries, self).setPoints(points)

            def updatePointXValuesIfNotPresent(self):
                pointStart = self.getDefPointStart()
                pointInterval = 3600000
                # 1 hour
                if isinstance(super(DateTimeSeries, self).getConfig(), BaseLineConfig):
                    config = super(DateTimeSeries, self).getConfig()
                    if config.getPointStart() is not None:
                        pointStart = config.getPointStart()
                    if config.getPointInterval() is not None:
                        pointInterval = config.getPointInterval()
                prevDate = Date(pointStart)
                count = 0
                for point in self.getPoints():
                    if (point.getX() is None) or (point.getX() is not None and point.isAutosetX()):
                        point.setAutosetX(True)
                        if count == 0:
                            point.setX(prevDate)
                            count += 1
                        else:
                            point.setX(self.getUpdatedDate(prevDate, pointInterval))
                            prevDate = point.getX()

            @classmethod
            def getDefPointStart(cls):
                cal = GregorianCalendar.getInstance()
                cal.set(Calendar.YEAR, 1970)
                cal.set(Calendar.MONTH, Calendar.JANUARY)
                cal.set(Calendar.DAY_OF_MONTH, 1)
                cal.set(Calendar.HOUR, 0)
                cal.set(Calendar.MINUTE, 0)
                cal.set(Calendar.SECOND, 0)
                cal.set(Calendar.MILLISECOND, 0)
                return cal.getTimeInMillis()

            @classmethod
            def getUpdatedDate(cls, dt, milliseconds):
                cal = Calendar.getInstance()
                cal.setTimeInMillis(dt.getTime() + milliseconds)
                return cal.getTime()

            def toString(self):
                return 'DateTimeSeries [includeTime=' + self._includeTime + ', getConfig()=' + InvientCharts_this.getConfig() + ', getName()=' + self.getName() + ', getType()=' + self.getType() + ', getStack()=' + self.getStack() + ', getXAxis()=' + self.getXAxis() + ', getYAxis()=' + self.getYAxis() + ']'

        return DateTimeSeries(*args, **kwargs)

    # *******************************************************************//
    # *************** Highcharts Configuration options ******************//
    # *******************************************************************//

    class SeriesType(object):
        COMMONSERIES = ['series']
        LINE = ['line']
        SPLINE = ['spline']
        SCATTER = ['scatter']
        AREA = ['area']
        AREASPLINE = ['areaspline']
        BAR = ['bar']
        COLUMN = ['column']
        PIE = ['pie']
        _type = None

        def __init__(self, type):
            self._type = type

        def getName(self):
            return self._type

        _values = [COMMONSERIES, LINE, SPLINE, SCATTER, AREA, AREASPLINE, BAR, COLUMN, PIE]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    SeriesType._enum_values = [SeriesType(*v) for v in SeriesType._enum_values]

    class SeriesCUR(Serializable):
        _type = None
        _name = None
        _reloadPoints = False
        _pointsAdded = LinkedHashSet()
        _pointsRemoved = LinkedHashSet()

        def getType(self):
            return self._type

        def getName(self):
            return self._name

        def __init__(self, *args):
            _0 = args
            _1 = len(args)
            if _1 == 2:
                type, name = _0
                super(SeriesCUR, self)()
                self._type = type
                self._name = name
            elif _1 == 3:
                type, name, reloadPoints = _0
                super(SeriesCUR, self)()
                self._type = type
                self._name = name
                self._reloadPoints = reloadPoints
            else:
                raise ARGERROR(2, 3)

        def isReloadPoints(self):
            """Indicates whether the client/terminal should update series by setting
            all data of a series instead of adding or removing individual points

            @return Returns true if the data of the series must be reloaded
                    otherwise false.
            """
            return self._reloadPoints

        def setReloadPoints(self, reloadPoints):
            self._reloadPoints = reloadPoints

        def trackPointAdded(self, point):
            self._pointsAdded.add(point)

        def trackPointRemoved(self, point):
            # If the point was added earlier and now removed
            # then there is no need to record its add/remove operation
            # as add of a point is nullified by remove of a point
            if not self.removePointIfTrackedAlready(point):
                self._pointsRemoved.add(point)

        def removePointIfTrackedAlready(self, point):
            # Used to clear all points added/removed when
            # series data is set/cleared using series.setPoints() or
            # series.removeAllPoints()
            return self._pointsAdded.remove(point)

        def clearTrackedPoints(self):
            self._pointsAdded.clear()
            self._pointsRemoved.clear()

        def getPointsAdded(self):
            return self._pointsAdded

        def getPointsRemoved(self):
            return self._pointsRemoved

        def hashCode(self):
            prime = 31
            result = 1
            result = (prime * result) + (0 if self._name is None else self._name.hashCode())
            result = (prime * result) + (0 if self._type is None else self._type.hashCode())
            return result

        def equals(self, obj):
            if self is obj:
                return True
            if obj is None:
                return False
            if self.getClass() != obj.getClass():
                return False
            other = obj
            if self._name is None:
                if other.name is not None:
                    return False
            elif not (self._name == other.name):
                return False
            if self._type is None:
                if other.type is not None:
                    return False
            elif not (self._type == other.type):
                return False
            return True

        def toString(self):
            return 'SeriesCUR [type=' + self._type + ', name=' + self._name + ', reloadPoints=' + self._reloadPoints + ', pointsAdded=' + self._pointsAdded + ', pointsRemoved=' + self._pointsRemoved + ']'

        class SeriesCURType(object):
            ADD = ['Add']
            UPDATE = ['Update']
            REMOVE = ['Remove']
            _name = None

            def __init__(self, name):
                self._name = name

            def getName(self):
                return self._name

            _values = [ADD, UPDATE, REMOVE]

            @classmethod
            def values(cls):
                return cls._enum_values[:]

        SeriesCURType._enum_values = [SeriesCURType(*v) for v in SeriesCURType._enum_values]

    _seriesCURMap = LinkedHashMap()

    def addSeriesCUROperation(self, newSeriesCUR):
        if self._seriesCURMap.keys().contains(newSeriesCUR.getName()):
            seriesCURSet = self._seriesCURMap.get(newSeriesCUR.getName())
            # If for a series, no operation is found
            if (seriesCURSet is None) or (len(seriesCURSet) == 0):
                seriesCURSet = LinkedHashSet()
                seriesCURSet.add(newSeriesCUR)
                self._seriesCURMap.put(newSeriesCUR.getName(), seriesCURSet)
            elif seriesCURSet.contains(newSeriesCUR):
                seriesCUR = self.getMatchedSeriesCUR(seriesCURSet, newSeriesCUR)
                # In case of series update (due to series.show/hide or
                # series.setPoints or series.removeAllPoints)
                # we need to check if all points of a series are set afresh. If
                # so then
                # set a flag to indicate that instead of adding and removing
                # points to and from series, set series data in full.
                if seriesCUR.getType() == SeriesCURType.UPDATE:
                    seriesCUR.setReloadPoints(newSeriesCUR.isReloadPoints())
                    if newSeriesCUR.isReloadPoints():
                        seriesCUR.clearTrackedPoints()
                    return True
                # Operation on a series has already been recorded
                return False
            else:
                seriesCURItr = seriesCURSet
                while seriesCURItr.hasNext():
                    seriesCUR = seriesCURItr.next()
                    if seriesCUR.getName() == newSeriesCUR.getName():
                        if (
                            SeriesCURType.REMOVE == newSeriesCUR.getType() and SeriesCURType.ADD == seriesCUR.getType()
                        ):
                            # Remove addition of a series as there is no reason
                            # to add
                            # a series and
                            # then remove it. E.g. If a new series is added and
                            # then
                            # removed then
                            # actually there is nothing to be done
                            seriesCURItr.remove()
                            return False
                        if (
                            SeriesCURType.UPDATE == newSeriesCUR.getType() and SeriesCURType.ADD == seriesCUR.getType()
                        ):
                            # There is no need for update as adding a series
                            # will
                            # take care of applying any update to the series
                            # attributes
                            # specifically visibility
                            return False
                        if (
                            SeriesCURType.REMOVE == newSeriesCUR.getType() and SeriesCURType.UPDATE == seriesCUR.getType()
                        ):
                            # Remove update of a series as there is no reason
                            # to update
                            # a series
                            # and then remove it. E.g. If an existing series
                            # was
                            # updated (for show/hide) and
                            # then removed then series need not be updated
                            # after all it
                            # is going to be
                            # removed. Hover, the remove operation must be
                            # captured.
                            seriesCURItr.remove()
                            break
            seriesCURSet.add(newSeriesCUR)
            return True
        else:
            seriesCURSet = LinkedHashSet()
            seriesCURSet.add(newSeriesCUR)
            self._seriesCURMap.put(newSeriesCUR.getName(), seriesCURSet)
            return True

    def addSeriesPointAddedOperation(self, seriesName, point):
        seriesCURSet = self._seriesCURMap.get(seriesName)
        if (seriesCURSet is None) or (len(seriesCURSet) == 0):
            seriesCUR = self.SeriesCUR(SeriesCURType.UPDATE, seriesName)
            seriesCUR.trackPointAdded(point)
            seriesCURSet = LinkedHashSet()
            seriesCURSet.add(seriesCUR)
            self._seriesCURMap.put(seriesName, seriesCURSet)
        else:
            lastSeriesCur = self.getLastSeriesCUR(seriesCURSet)
            # Track points only if series is updated.
            # Tracking point is useless in following cases
            # 1. A new series is added : In this case, a series will be added
            # with all points so no need to track
            # 2. A series is removed : In this case, a series will be removed
            # and hence any point added to the series doesn't carry any
            # meaning.
            if (
                lastSeriesCur.getType() == SeriesCURType.UPDATE and not lastSeriesCur.isReloadPoints()
            ):
                lastSeriesCur.trackPointAdded(point)

    def getLastSeriesCUR(self, seriesCURSet):
        if (seriesCURSet is None) or (len(seriesCURSet) == 0):
            return None
        lastSeriesCur = None
        for seriesCur in seriesCURSet:
            lastSeriesCur = seriesCur
        return lastSeriesCur

    def getMatchedSeriesCUR(self, seriesCURSet, matchAgainstSeriesCUR):
        for seriesCur in seriesCURSet:
            if matchAgainstSeriesCUR == seriesCur:
                return seriesCur
        return None

    def addSeriesPointRemovedOperation(self, seriesName, point):
        seriesCURSet = self._seriesCURMap.get(seriesName)
        if (seriesCURSet is None) or (len(seriesCURSet) == 0):
            seriesCUR = self.SeriesCUR(SeriesCURType.UPDATE, seriesName)
            seriesCUR.trackPointRemoved(point)
            seriesCURSet = LinkedHashSet()
            seriesCURSet.add(seriesCUR)
            self._seriesCURMap.put(seriesName, seriesCURSet)
        else:
            lastSeriesCur = self.getLastSeriesCUR(seriesCURSet)
            # Track points only if series is updated.
            # Tracking point is useless in following cases
            # 1. A new series is added : In this case, a series will be added
            # with all points so no need to track
            # 2. A series is removed : In this case, a series will be removed
            # and hence any point removed from the series
            # doesn't carry any meaning.
            if (
                lastSeriesCur.getType() == SeriesCURType.UPDATE and not lastSeriesCur.isReloadPoints()
            ):
                lastSeriesCur.trackPointRemoved(point)

    def refresh(self):
        """After a series is added or removed, there is no need to call this method
        as it is handled implicitly. This method will send updates to the client.
        This method should be called after adding/removing plotbands and
        plotlines. This inconsistency will be fixed in next revision.
        """
        super(InvientCharts, self).requestRepaint()

    def print_(self):
        """Displays a Print dialog of the Webkit to print this chart. Invoking this
        method causes the Webkit to hide other widgets on the screen and only
        this chart widget will be visible. Also it prints this chart widget as it
        is displayed.
        """
        self._isPrint = True
        self.requestRepaint()



class MousePosition(object):
    """This class contain mouse coordinates when a click event occurs
    on a chart, a series or a point.

    The mouse coordinates are in pixels.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, mouseX, mouseY):
        """Creates this object with given arguments.

        @param mouseX:
                   x position of mouse when a click event occurred, in pixel
        @param mouseY:
                   y position of mouse when a click event occurred, in pixel
        """
        self._mouseX = mouseX
        self._mouseY = mouseY


    def getMouseX(self):
        """@return: Returns x position of mouse when a click event occurred,
        in pixel
        """
        return self._mouseX


    def getMouseY(self):
        """@return: Returns y position of mouse when a click event occurred,
        in pixel
        """
        return self._mouseY


    def __str__(self):
        return ('MousePosition [mouseX=' + self._mouseX
                + ', mouseY=' + self._mouseY + ']')


class PointEventData(object):

    def __init__(self, seriesName, category, pointX, pointY):
        super(PointEventData, self).__init__()
        self._seriesName = seriesName
        self._category = category
        self._pointX = pointX
        self._pointY = pointY

    def getSeriesName(self):
        return self._seriesName

    def getCategory(self):
        return self._category

    def getPointX(self):
        return self._pointX

    def getPointY(self):
        return self._pointY

    def __str__(self):
        return ('PointEventData [seriesName=' + self._seriesName
                + ', category=' + self._category
                + ', pointX=' + self._pointX
                + ', pointY=' + self._pointY + ']')


class PointClickEvent(ComponentEvent):
    """Click event. This event is thrown, when any point of this chart is
    clicked and the point marker is enabled. The point marker is enabled by
    default.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, category, point, mousePosition):
        """New instance of the point click event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param category:
                   a category to which point is associated in case of
                   categorized axis,
        @param point:
                   the point on which the click event occurred
        @param mousePosition:
                   the position of a mouse when the click event occurred
        """
        super(PointClickEvent, self)(source)
        self._chart = chart
        self._category = category
        self._point = point
        self._mousePosition = mousePosition

    def getCategory(self):
        """@return: Returns a category to which point is associated in case
        of categorized axis only.
        """
        return self._category

    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart

    def getPoint(self):
        """@return: Returns the point on which the click event occurred"""
        return self._point

    def getMousePosition(self):
        """@return: Returns the position of a mouse when the click event
        occurred"""
        return self._mousePosition


class PointClickListener(object):
    """Interface for listening for a L{PointClickEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def pointClick(self, pointClickEvent):
        pass


class PointRemoveEvent(ComponentEvent):
    """Point remove event. This event is thrown, when any point of this chart
    is removed from its series.

    This event is EXPERIMENTAL ONLY.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, category, point):
        """New instance of the point remove event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param category:
                   a category to which point is associated in case of
                   categorized axis,
        @param point:
                   the point removed
        """
        super(PointRemoveEvent, self).__init__(source)
        self._chart = chart
        self._category = category
        self._point = point


    def getCategory(self):
        """@return: Returns a category to which point is associated in case
        of categorized axis only.
        """
        return self._category


    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart


    def getPoint(self):
        """@return: Returns the point which has been removed"""
        return self._point


class PointRemoveListener(object):
    """Interface for listening for a L{PointRemoveEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def pointRemove(self, pointRemoveEvent):
        pass


class PointUnselectEvent(ComponentEvent):
    """Point unselect event. This event is thrown, when any point of this
    chart is unselected and the point marker is enabled. The point marker
    is enabled by default.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, category, point):
        """New instance of the point unselect event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param category:
                   a category to which point is associated in case of
                   categorized axis,
        @param point:
                   the point unselected as a result of this event
        """
        super(PointUnselectEvent, self).__init__(source)
        self._chart = chart
        self._category = category
        self._point = point


    def getCategory(self):
        """@return: Returns a category to which point is associated in case
        of categorized axis only.
        """
        return self._category


    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart


    def getPoint(self):
        """@return: Returns the unselected point"""
        return self._point


class PointUnselectListener(object):
    """Interface for listening for a L{PointUnselectEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def pointUnSelect(self, pointUnSelectEvent):
        pass


class PointSelectEvent(ComponentEvent):
    """Point select event. This event is thrown, when any point of this chart
    is selected and the point marker is enabled. The point marker is enabled
    by default.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, category, point):
        """New instance of the point select event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param category:
                   a category to which point is associated in case of
                   categorized axis,
        @param point:
                   the point selected as a result of this event
        """
        super(PointSelectEvent, self).__init__(source)
        self._chart = chart
        self._category = category
        self._point = point


    def getCategory(self):
        """@return: Returns a category to which point is associated in case
        of categorized axis only.
        """
        return self._category


    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart


    def getPoint(self):
        """@return: Returns the selected point"""
        return self._point


class PointSelectListener(object):
    """Interface for listening for a L{PointSelectListener} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def pointSelected(self, pointSelectEvent):
        pass


_POINT_CLICK_METHOD = getattr(PointClickListener, 'pointClick')
_POINT_REMOVE_METHOD = getattr(PointRemoveListener, 'pointRemove')
_POINT_SELECT_METHOD = getattr(PointSelectListener, 'pointSelected')
_POINT_UNSELECT_METHOD = getattr(PointUnselectListener, 'pointUnSelect')




class SeriesClickEvent(ComponentEvent):
    """Series click event. This event is thrown, when any series of this chart
    is clicked.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, series, point, mousePosition):
        """New instance of the series click event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param series:
                   the series on which click event occurred
        @param point:
                   the closest point of a series
        @param mousePosition:
                   the position of a mouse when the click event occurred
        """
        super(SeriesClickEvent, self).__init__(source)
        self._chart = chart
        self._series = series
        self._point = point
        self._mousePosition = mousePosition


    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart


    def getSeries(self):
        """@return: Returns the series object on which the click event occurred"""
        return self._series


    def getNearestPoint(self):
        """@return: Returns the point of a series closest to the position where
        mouse click event occurred.
        """
        return self._point


    def getMousePosition(self):
        """@return: Returns the position of a mouse when the click event
        occurred"""
        return self._mousePosition


class SeriesClickListerner(object):
    """Interface for listening for a L{SeriesClickListerner} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def seriesClick(self, seriesClickEvent):
        pass


class SeriesHideEvent(ComponentEvent):
    """Series Hide event. This event is thrown, when any series of this chart
    is hidden.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, series):
        """@param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param series:
                   the series which got hidden
        """
        super(SeriesHideEvent, self).__init__(source)
        self._chart = chart
        self._series = series


    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart


    def getSeries(self):
        """@return: Returns the series which got hidden"""
        return self._series


class SeriesHideListerner(object):
    """Interface for listening for a L{SeriesHideEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def seriesHide(self, seriesHideEvent):
        pass


class SeriesShowEvent(ComponentEvent):
    """Series show event. This event is thrown, when any series of this chart
    is displayed after a chart is created.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, series):
        """New instance of the series show event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param series:
                   the series which got displayed
        """
        super(SeriesShowEvent, self).__init__(source)
        self._chart = chart
        self._series = series


    def getChart(self):
        """@return: Returns the chart object associated with the series"""
        return self._chart


    def getSeries(self):
        """@return: Returns the series which got displayed"""
        return self._series


class SeriesShowListerner(object):
    """Interface for listening for a L{SeriesShowEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def seriesShow(self, seriesShowEvent):
        pass


class SeriesLegendItemClickEvent(ComponentEvent):
    """Series legend item click event. This event is thrown, when legend item
    is clicked. This event is not applicable for PieChart instead use
    L{LegendItemClickEvent}

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, series):
        """New instance of the point click event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param series:
                   the series associated with the legend item
        """
        super(SeriesLegendItemClickEvent, self).__init__(source)
        self._chart = chart
        self._series = series


    def getChart(self):
        """@return: Returns the chart object associated with the series"""
        return self._chart


    def getSeries(self):
        """@return: Returns the series associated with the legend item"""
        return self._series


class SeriesLegendItemClickListerner(object):
    """Interface for listening for a L{SeriesLegendItemClickEvent}
    triggered by L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def seriesLegendItemClick(self, seriesLegendItemClickEvent):
        pass


_SERIES_CLICK_METHOD = getattr(SeriesClickListerner, 'seriesClick')
_SERIES_HIDE_METHOD = getattr(SeriesHideListerner, 'seriesHide')
_SERIES_SHOW_METHOD = getattr(SeriesShowListerner, 'seriesShow')
_SERIES_LEGENDITEM_CLICK_METHOD = getattr(SeriesLegendItemClickListerner,
        'seriesLegendItemClick')


class PieChartLegendItemClickEvent(ComponentEvent):
    """PieChart legend item click event. This event is thrown, when the legend
    item belonging to the pie point (slice) is clicked.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, point):
        """New instance of the piechart legend item click event

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param point:
                   the pie point (slice) associated with the legend item
        """
        super(PieChartLegendItemClickEvent, self).__init__(source)
        self._chart = chart
        self._point = point


    def getChart(self):
        """@return: Returns the chart object associated with the point"""
        return self._chart


    def getPoint(self):
        """@return: Returns the pie point (slice) associated with the legend
        item"""
        return self._point


class PieChartLegendItemClickListener(object):
    """Interface for listening for a L{PieChartLegendItemClickEvent}
    triggered by L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def legendItemClick(self, legendItemClickEvent):
        pass


_LEGENDITEM_CLICK_METHOD = getattr(PieChartLegendItemClickListener,
        'legendItemClick')


class ChartClickEvent(ComponentEvent):
    """Chart Click event. This event is thrown, when this chart is clicked.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, point, mousePosition):
        """New instance of the chart click event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param point:
                   the position where the click event occurred in axes units
        @param mousePosition:
                   the coordinate of mouse where the click event occurred in
                   pixels
        """
        super(ChartClickEvent, self).__init__(source)
        self._chart = chart
        self._point = point
        self._mousePosition = mousePosition


    def getChart(self):
        """Returns the chart object on which the click event occurred

        @return: Returns the chart object on which the click event occurred
        @see: L{InvientCharts}
        """
        return self._chart


    def getPoint(self):
        """Returns the point representing the position where the click event
        occurred in axes units

        @return: Returns the point representing the position where the click
                 event occurred in axes units
        @see: L{Point}
        """
        return self._point


    def getMousePosition(self):
        """Returns the position of a mouse when the click event occurred

        @return: Returns the position of a mouse when the click event occurred
        @see: L{MousePosition}
        """
        return self._mousePosition


    def __str__(self):
        return ('ChartClickEvent [point=' + self._point
                + ', mousePosition=' + self._mousePosition + ']')


class ChartClickListener(object):
    """Interface for listening for a L{ChartClickEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def chartClick(self, chartClickEvent):
        pass


class ChartAddSeriesEvent(ComponentEvent):
    """Add series event. This event is thrown, when a series is added to the
    chart.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart):
        """New instance of the chart add series event.

        @param source
        @param chart
        """
        super(ChartAddSeriesEvent, self).__init__(source)
        self._chart = chart

    def getChart(self):
        """Returns the chart object to which a series is added

        @return: Returns the chart object to which a series has been added.
        @see: L{InvientCharts}
        """
        return self._chart


class ChartAddSeriesListener(object):
    """Interface for listening for a L{ChartAddSeriesEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def chartAddSeries(self, chartAddSeriesEvent):
        pass


class ChartArea(object):
    """Defines information on the selected area.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, xAxisMin, xAxisMax, yAxisMin, yAxisMax):
        self._xAxisMin = xAxisMin
        self._xAxisMax = xAxisMax
        self._yAxisMin = yAxisMin
        self._yAxisMax = yAxisMax

    def getxAxisMin(self):
        return self._xAxisMin

    def getxAxisMax(self):
        return self._xAxisMax

    def getyAxisMin(self):
        return self._yAxisMin

    def getyAxisMax(self):
        return self._yAxisMax

    def __str__(self):
        return ('ChartSelectedArea [xAxisMin=' + self._xAxisMin
                + ', xAxisMax=' + self._xAxisMax
                + ', yAxisMin=' + self._yAxisMin
                + ', yAxisMax=' + self._yAxisMax + ']')


class ChartZoomEvent(ComponentEvent):
    """Chart zoom event. This event is thrown, when an area of the chart has
    been selected.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, chartArea):
        """New instance of the chart zoom event.

        @param source
                   the chart object itself
        @param chart
                   the chart object itself
        @param chartArea
                   the chartArea object containing dimensions of zoomed area
                   of the chart
        """
        super(ChartZoomEvent, self).__init__(source)
        self._chart = chart
        self._chartArea = chartArea


    def getChart(self):
        """Returns the chart object for which the zoom event has occurred

        @return: Returns the chart object for which the zoom event has
                 occurred
        """
        return self._chart


    def getChartArea(self):
        """Returns the chartArea object containing dimensions of zoomed area
        of the chart

        @return: Returns the chartArea object containing dimensions of zoomed
                 area of the chart
        """
        return self._chartArea


class ChartZoomListener(object):
    """Interface for listening for a L{ChartZoomEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def chartZoom(self, chartZoomEvent):
        pass


class ChartResetZoomEvent(ComponentEvent):
    """Chart reset zoom event. This event is thrown, when a chart is reset
    by setting its zoom level to normal.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart):
        """New instance of the chart reset zoom event

        @param source
                   the chart object itself
        @param chart
                   the chart object itself
        """
        super(ChartResetZoomEvent, self).__init__(source)
        self._chart = chart


    def getChart(self):
        """Returns the chart object for which zoom has been reset to normal

        @return: Returns the chart object for which zoom has been reset to
                 normal
        """
        return self._chart


class ChartResetZoomListener(object):
    """Interface for listening for a L{@link ChartResetZoomEvent} triggered by
    L{InvientCharts}

    @author: Invient
    @author: Richard Lincoln
    """

    def chartResetZoom(self, chartResetZoomEvent):
        pass


class ChartSVGAvailableEvent(ComponentEvent):
    """Chart SVG event. This event is thrown, when an SVG string representing
    the chart is received or ready.

    Note that this event is thrown only once after a
    L{ChartSVGAvailableListener} is registered.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, source, chart, svg):
        """New instance of the chart svg available event.

        @param source:
                   the chart object itself
        @param chart:
                   the chart object itself
        @param svg:
                   an svg string representing the chart object
        """
        super(ChartSVGAvailableEvent, self).__init__(source)
        self._chart = chart
        self._svg = svg


    def getChart(self):
        """Returns the chart object for which an svg string representation
        is available

        @return: Returns the chart object for which an svg string
                 representation is available
        """
        return self._chart


    def getSVG(self):
        """@return: Returns an SVG string representing the chart"""
        return self._svg


class ChartSVGAvailableListener(object):
    """Interface for listening for a L{ChartSVGAvailableEvent} triggered by
    L{InvientCharts}.

    The chart can have only one listener of this type registered at any time.
    If a listener has already been registered and an attempt is made to
    register another listener then the previously registered listener will be
    unregistered and the new listener will be registered.

    A listener will be called only once after it has been registered though
    it will be called again if the same listener is registered again.

    @author: Invient
    @author: Richard Lincoln
    """

    def svgAvailable(self, chartSVGAvailableEvent):
        pass


_CHART_CLICK_METHOD = getattr(ChartClickListener, 'chartClick')
_CHART_ADD_SERIES_METHOD = getattr(ChartAddSeriesListener, 'chartAddSeries')
_CHART_ZOOM_METHOD = getattr(ChartZoomListener, 'chartZoom')
_CHART_RESET_ZOOM_METHOD = getattr(ChartResetZoomListener, 'chartResetZoom')
_CHART_SVG_AVAILABLE_METHOD = getattr(ChartSVGAvailableListener, 'svgAvailable')


class Point(object):
    """This class represents a point of the chart's series. A series can have
    one or more points. A point has (X, Y) coordinates. None of the
    coordinates are mandatory. The name of a point can be displayed in a
    tooltip.

    To represent no activity or missing points in the chart, create a point
    with both X and Y as null or just Y as null.

    It is possible to specify custom configuration for each point. e.g. If a
    highest point can be marked in a chart with a different color using this
    configuration.

    A point cannot be created without a series. It must belong to a series.
    However, the point must be added to a series by calling Series.addPoint()
    or Series.setPoints() to permanently add point to the series.

    @author: Invient
    @author: Richard Lincoln

    @see: L{DecimalPoint}
    @see: L{DateTimePoint}
    @see: L{PointConfig}
    """
    _id = None
    _name = None
    _series = None
    _config = None
    _isAutosetX = None
    _shift = None

    def __init__(self, series, name_or_config=None, config=None):
        """Creates a point with given arguments.

        @param series
                   The series to which the point must be associated.
        @exception IllegalArgumentException
                       If the argument series is null
        ---
        To allow creation of a point from inside of InvientCharts component
        ---
        Creates a point with given arguments.

        @param series
                   The series to which the point must be associated.
        @param config
                   The configuration for this point, if any
        @exception IllegalArgumentException
                       If the argument series is null
        ---
        Creates a point with given arguments.

        @param series
                   The series to which the point must be associated.
        @param name
                   name of this point
        @exception IllegalArgumentException
                       If the argument series is null
        ---
        Creates a point with given arguments.

        @param series
                   The series to which the point must be associated.
        @param name
                   name of this point
        @param config
                   The configuration for this point, if any
        @exception IllegalArgumentException
                       If the argument series is null
        """
        if name_or_config is not None:
            if isinstance(name_or_config, PointConfig):
                config = name_or_config
                name = None
            else:
                name = name_or_config
                config = None

        self._series = series
        self._name = name
        self._config = config


    def getId(self):
        return self._id


    def getName(self):
        """@return: Returns name of this point"""
        return self._name


    def setName(self, name):
        """Sets name of this point

        @param name:
                   name of this point
        """
        self._name = name


    def getSeries(self):
        """@return: Returns L{Series} associated with this point"""
        return self._series


    def getConfig(self):
        """@return: Returns L{PointConfig} for this point"""
        return self._config


    def setConfig(self, config):
        """Sets L{PointConfig} for this point

        @param config:
                   configuration of this point
        @see: L{PointConfig}
        """
        self._config = config


    def isAutosetX(self):
        """@return: Returns true if X value of this point is set
        programmatically"""
        return self._isAutosetX


    def setAutosetX(self, isAutosetX):
        """If the argument is true it indicates that the X value of this point
        is set programmatically and user has not specified it.
        """
        self._isAutosetX = isAutosetX


    def isShift(self):
        """@return: Returns true if a point at the start of the series should
        beshifted off when this point is appended otherwise false.
        """
        return self._shift


    def setShift(self, shift):
        """A value of true means one point is shifted off the start of the
        series as one is appended to the end.
        """
        self._shift = shift


    def getX(self):
        """@return: Returns X value of this point"""
        pass


    def getY(self):
        """@return: Returns Y value of this point"""
        pass


    def __str__(self):
        return ('Point [id=' + self._id
                + ', name=' + self._name
                + ', series=' + self._series.getName()
                + ', config=' + self._config + ']')


class DecimalPoint(Point):
    """This class represent a point with (X, Y) both as number. It should be
    used to add points to L{XYSeries}

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, *args):
        """@param series
                   the series to which this belongs to
        ---
        @param series
                   the series to which this point belongs to
        @param y
                   the y value of this point
        ---
        @param series
                   the series to which this belongs to
        @param name
                   the name of this point
        @param y
                   the y value of this point
        ---
        To allow creation of a point within the InvientChart.

        @param x
                   the x value of this point
        @param y
                   the y value of this point
        ---
        @param series
                   the series to which this belongs to
        @param name
                   the name for this point
        @param y
                   the y value of this point
        @param config
        ---
        @param series
                   the series to which this belongs to
        @param y
                   the y value of this point
        @param config
                   the configuration for this point
        ---
        @param series
                   the series to which this belongs to
        @param x
                   the x value of this point
        @param y
                   the y value of this point
        ---
        @param series
                   the series to which this belongs to
        @param x
                   the x value of this point
        @param y
                   the y value of this point
        ---
        @param series
                   the series to which this belongs to
        @param x
                   the x value of this point
        @param y
                   the y value of this point
        @param config
                   the configuration of this point
        ---
        @param series
                   the series to which this belongs to
        @param x
                   the x value of this point
        @param y
                   the y value of this point
        @param config
                   the configuration of this point
        """
        nargs = len(args)
        if nargs == 1:
            series, = args
            super(DecimalPoint, self).__init__(series)
        elif nargs == 2:
            if isinstance(args[0], Series):
                series, y = args
                super(DecimalPoint, self).__init__(series)
                self._y = y
            else:
                x, y = args
                super(DecimalPoint, self).__init__()
                self._x = x
                self._y = y
        elif nargs == 3:
            if isinstance(args[1], float):
                if isinstance(args[2], PointConfig):
                    series, y, config = args
                    super(DecimalPoint, self).__init__(series, config)
                    self._y = y
                else:
                    series, x, y = args
                    self.__init__(series, x, y, None)
                    series, x, y = args
                    self.__init__(series, x, y, None)
            else:
                series, name, y = args
                super(DecimalPoint, self).__init__(series, name)
                self._y = y
        elif nargs == 4:
            if isinstance(args[1], float):
                series, x, y, config = args
                super(DecimalPoint, self).__init__(series, config)
                self._x = x
                self._y = y
                series, x, y, config = args
                super(DecimalPoint, self).__init__(series, config)
                self._x = x
                self._y = y
            else:
                series, name, y, config = args
                super(DecimalPoint, self).__init__(series, name, config)
                self._y = y
        else:
            raise ValueError


    def getX(self):
        return self._x


    def setX(self, x):
        """Sets the x value of this point

        @param x
        """
        self._x = x


    def getY(self):
        return self._y


    def setY(self, y):
        """Sets the y value of this point

        @param y
        """
        self._y = y


    def __str__(self):
        return ('DecimalPoint [x=' + self._x
                + ', y=' + self._y
                + ', id=' + self.getId()
                + ', name=' + self.getName()
                + ', seriesName=' + (InvientCharts_this.getSeries().getName() if InvientCharts_this.getSeries() is not None else '') + ']')


    def __hash__(self):
        prime = 31
        result = 1
        result = (prime * result) + (0 if self._y is None else self._y.__hash__())
        return result


    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        # If x is null then return always false as x is calculated if not
        # specified
        if (self._x is None) or (other.x is None):
            return False
        if not (self._x == other.x):
            return False
        if self._y is None:
            if other.y is not None:
                return False
        elif other.y is None:
            return False
        elif self._y.compareTo(other.y) != 0:
            return False
        return True


class DateTimePoint(Point):
    """This class represent a point with (X, Y) both as number. It should be
    used to add points to {@link DateTimeSeries}

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, *args):
        """@param series
                   the series to which this belongs to
        ---
        @param series
                   the series to which this belongs to
        @param y
                   the y value of this point
        ---
        @param series
                   the series to which this belongs to
        @param name
                   the name of this point
        @param y
                   the y value of this point
        ---
        @param series
                   the series to which this belongs to
        @param name
                   the name of this point
        @param y
                   the y value of this point
        @param config
        ---
        @param series
                   the series to which this belongs to
        @param x
                   the x value of this point
        @param y
                   the y value of this point
        """
        args = args
        nargs = len(args)
        if nargs == 1:
            series, = args
            super(DateTimePoint, self).__init__(series)
        elif nargs == 2:
            series, y = args
            self.__init__(series, '', y)
        elif nargs == 3:
            if isinstance(args[1], datetime):
                series, x, y = args
                self.__init__(series, y)
                self._x = x
            else:
                series, name, y = args
                super(DateTimePoint, self).__init__(series, name)
                self._y = y
        elif nargs == 4:
            series, name, y, config = args
            super(DateTimePoint, self).__init__(series, name, config)
            self._y = y
        else:
            raise ValueError


    def getX(self):
        return self._x


    def setX(self, x):
        """Sets the x value of this point

        @param x
        """
        self._x = x


    def getY(self):
        return self._y


    def setY(self, y):
        """Sets the y value of this point

        @param y
        """
        self._y = y


    def __str__(self):
        return 'DateTimePoint [x=' + InvientCharts_this.getDateInMilliseconds(self._x, InvientCharts_this.getSeries().isIncludeTime() if InvientCharts_this.getSeries() is not None else False) + ', y=' + self._y + ', id=' + self.getId() + ', name=' + self.getName() + ', seriesName=' + (InvientCharts_this.getSeries().getName() if InvientCharts_this.getSeries() is not None else '') + ']'


    def __hash__(self):
        prime = 31
        result = 1
        result = (prime * result) + (0 if self._y is None else self._y.__hash__())
        return result


    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        # If x is null then return always false as x is calculated if not
        # specified
        if (self._x is None) or (other.x is None):
            return False
        pointIncludeTime = self.getSeries().isIncludeTime() if isinstance(self.getSeries(), InvientCharts_this.DateTimeSeries) else False
        pointOtherIncludeTime = other.getSeries().isIncludeTime() if isinstance(other.getSeries(), InvientCharts_this.DateTimeSeries) else False
        pointX = InvientCharts_this.getDateInMilliseconds(self._x, pointIncludeTime)
        pointOtherX = InvientCharts_this.getDateInMilliseconds(other.x, pointOtherIncludeTime)
        if pointX.compareTo(pointOtherX) != 0:
            return False
        if self._y is None:
            if other.y is not None:
                return False
        elif other.y is None:
            return False
        elif self._y.compareTo(other.y) != 0:
            return False
        return True


class Series(object):
    """This class defines a series of the chart. A series contains a collection
    of points. Series can be one of types defined by L{SeriesType}.

    Each series must have unique name. If an attempt is made to add two
    series with same then only the first added series will be in effect.

    If the series type is not specified, it defaults to chart type and the
    default chart type is SeriesType.LINE. A series has unique xAxis and
    yAxis object associated with it. There is no need to set xAxis and yAxis
    unless the chart has more than one one axis of any type and the series
    must belong to any of the secondary axis.

    It is also possible to specify configuration for individual series and
    not just series type.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, name, seriesType_or_config=None, config=None):
        """Creates a series with given name, type and configuration

        @param name:
                   the name of this series
        @param seriesType_or_config:
                   the type of this series or the configuration for this series
        @param config:
                   the configuration for this series
        """
        self._points = set()
        self._name = ''
        self._type = None
        self._stack = None
        self._xAxis = None
        self._yAxis = None
        self._config = None
        self._invientCharts = None

        if seriesType_or_config is not None:
            if isinstance(seriesType_or_config, SeriesType):
                seriesType = seriesType_or_config
            else:
                config = seriesType_or_config
                seriesType = None

        self._name = name
        self._type = seriesType
        self._config = config


    def getConfig(self):
        """@return: Returns the configuration object associated with this
        series"""
        return self._config


    def getName(self):
        """@return: Returns name of this series"""
        return self._name


    def setName(self, name):
        """Sets name of this series

        @param name
        """
        self._name = name


    def getType(self):
        """@return"""
        return self._type


    def setType(self, typ):
        """Sets type of this series

        @param typ
        """
        self._type = typ


    def getStack(self):
        """@return: Returns stack of this series"""
        return self._stack


    def setStack(self, stack):
        """By using this stack property, it is possible to group series in a
        stacked chart. Sets stack for this series. If two series belongs to
        the same stack then the resultant chart will be stacked chart

        @param stack
        """
        self._stack = stack


    def getXAxis(self):
        """@return: Returns x-axis associated with this series.
        @see: L{Axis}
        """
        return self._xAxis


    def setXAxis(self, xAxis):
        """Sets x-axis of this series. A series can be associated with at most
        one x-axis.

        @param xAxis
        """
        self._xAxis = xAxis


    def getYAxis(self):
        """@return: Returns y-axis of this series."""
        return self._yAxis


    def setYAxis(self, yAxis):
        """Sets y-axis of this series. A series can be associated with at most
        one y-axis.

        @param yAxis
        """
        self._yAxis = yAxis


    def removePoint(self, *points):
        """@param points"""
        pointsRemovedList = list()
        for point in points:
            if self._points.remove(point):
                pointsRemovedList.append(point)

        self.updatePointXValuesIfNotPresent()

        for point in pointsRemovedList:
            if self._invientCharts is not None:
                self._invientCharts.addSeriesPointRemovedOperation(point.getSeries().getName(), point)
                self._invientCharts.requestRepaint()


    def removeAllPoints(self):
        """Removes all points in this series"""
        self._points.clear()
        if self._invientCharts is not None:
            self._invientCharts.addSeriesCUROperation(SeriesCUR(SeriesCURType.UPDATE, self.getName(), True))
            self._invientCharts.requestRepaint()


    def addPoint(self, shift, *points):
        """Adds one or more points into this series, specified as an argument
        to this method

        @param points
        @return: Returns null if the argument is null otherwise returns a
                 collection of points which are added in this series. If a
                 point has same (x, y) value as any other point in the
                 argument points then it will not be added.
        """
        if shift:
            # Remove first point as other points gets appended at the end
            pointsItr = self._points
            if pointsItr.hasNext():
                pointsItr.next()
                pointsItr.remove()
        pointsAddedList = list()
        for point in points:
            if self._points.add(point):
                pointsAddedList.add(point)
        self.updatePointXValuesIfNotPresent()
        # Now record point add event as we need to know x value of a point
        for point in pointsAddedList:
            if self._invientCharts is not None:
                self._invientCharts.addSeriesPointAddedOperation(point.getSeries().getName(), point)
                self._invientCharts.requestRepaint()
        return LinkedHashSet(pointsAddedList)

    def addPointsInternal(self, points):
        for point in points:
            self._points.add(point)

    def getPoints(self):
        """@return Returns all points of this series. Adding or removing any
                point to or from the returned collection will not impact the
                chart. To add a point or points, use addPoint() or
                removePoint() method.
        """
        return LinkedHashSet(self._points)

    def setPoints(self, points):
        """Sets points into this series

        @param points
        @return Returns null if the argument is null otherwise returns a
                collection of points which are set in this series. If a point
                has same (x, y) value as any other point in the argument
                points then it will not be added.
        """
        if points is not None:
            self._points.clear()
            self.addPointsInternal(points)
            self.updatePointXValuesIfNotPresent()
            if self._invientCharts is not None:
                self._invientCharts.addSeriesCUROperation(InvientCharts_this.SeriesCUR(SeriesCURType.UPDATE, self.getName(), True))
                self._invientCharts.requestRepaint()
            return self.getPoints()
        return None

    def updatePointXValuesIfNotPresent(self):
        """Each of the subclass needs to implement this method to ensure that
        each point has appropriate X value even if it is not specified.
        """
        pass

    def show(self):
        """Show this series"""
        self._config = SeriesConfig() if self._config is None else self._config
        self._config.setVisible(True)
        if self._invientCharts is not None:
            self._invientCharts.addSeriesCUROperation(InvientCharts_this.SeriesCUR(SeriesCURType.UPDATE, self.getName()))
            self._invientCharts.requestRepaint()

    def hide(self):
        """Hide this series"""
        self._config = SeriesConfig() if self._config is None else self._config
        self._config.setVisible(False)
        if self._invientCharts is not None:
            self._invientCharts.addSeriesCUROperation(InvientCharts_this.SeriesCUR(SeriesCURType.UPDATE, self.getName()))
            self._invientCharts.requestRepaint()

    def setInvientCharts(self, invientCharts):
        self._invientCharts = invientCharts

    def hashCode(self):
        prime = 31
        result = 1
        result = (prime * result) + (0 if self._name is None else self._name.hashCode())
        return result

    def equals(self, obj):
        if self is obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        if self._name is None:
            if other.name is not None:
                return False
        elif not (self._name == other.name):
            return False
        return True

    def toString(self):
        return 'Series [points=' + self._points + ', name=' + self._name + ', type=' + self._type + ', stack=' + self._stack + ', xAxis=' + self._xAxis + ', yAxis=' + self._yAxis + ', config=' + self._config + ']'