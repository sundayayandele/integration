/*
 * ============LICENSE_START=======================================================
 * org.onap.integration
 * ================================================================================
 * Copyright (C) 2018 NOKIA Intellectual Property. All rights reserved.
 * ================================================================================
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============LICENSE_END=========================================================
 */

package org.onap.pnfsimulator.message;

public final class MessageConstants {

    public static final String DOMAIN = "domain";
    public static final String EVENT_ID = "eventId";
    public static final String EVENT_TYPE = "eventType";
    public static final String LAST_EPOCH_MICROSEC = "lastEpochMicrosec";
    public static final String PRIORITY = "priority";
    public static final String SEQUENCE = "sequence";
    public static final String START_EPOCH_MICROSEC = "startEpochMicrosec";
    public static final String INTERNAL_HEADER_FIELDS = "internalHeaderFields";
    public static final String VERSION = "version";
    public static final String OTHER_FIELDS_VERSION = "otherFieldsVersion";
    public static final String PNF_LAST_SERVICE_DATE = "pnfLastServiceDate";
    public static final String PNF_MANUFACTURE_DATE = "pnfManufactureDate";

    // mandatory
    public static final String PNF_OAM_IPV4_ADDRESS = "pnfOamIpv4Address";
    public static final String PNF_OAM_IPV6_ADDRESS = "pnfOamIpv6Address";
    public static final String PNF_SERIAL_NUMBER = "pnfSerialNumber";
    public static final String PNF_VENDOR_NAME = "pnfVendorName";

    public static final String PNF_PREFIX = "pnf";
    public static final String COMMON_EVENT_HEADER = "commonEventHeader";
    public static final String OTHER_FIELDS = "otherFields";
    public static final String TEST_DURATION = "testDuration";
    public static final String MESSAGE_INTERVAL = "messageInterval";

    private MessageConstants() {
    }

}